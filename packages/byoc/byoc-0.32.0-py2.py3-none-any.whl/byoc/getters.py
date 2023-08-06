#!/usr/bin/env python3

from . import model
from .model import UNSPECIFIED
from .cast import Context, call_with_context
from .meta import GetterMeta, LayerMeta
from .errors import ApiError, NoValueFound
from operator import attrgetter
from more_itertools import value_chain, always_iterable

class Getter:

    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def __repr__(self):
        cls = f'byoc.{self.__class__.__name__}'
        args = self.__reprargs__()
        kwargs = [f'{k}={v!r}' for k, v in self.kwargs.items()]
        return f'{cls}({", ".join((*args, *kwargs))})'

    def __reprargs__(self):
        return []  # pragma: no cover

    def bind(self, obj, param):
        raise NotImplementedError

class Key(Getter):

    def __init__(self, config_cls, key=UNSPECIFIED, **kwargs):
        super().__init__(**kwargs)
        self.config_cls = config_cls
        self.key = key

    def __reprargs__(self):
        if self.key is UNSPECIFIED:
            return [self.config_cls.__name__]
        else:
            return [self.config_cls.__name__, repr(self.key)]

    def bind(self, obj, param):
        wrapped_configs = [
                wc for wc in model.get_wrapped_configs(obj)
                if isinstance(wc.config, self.config_cls)
        ]
        return BoundKey(self, obj, param, wrapped_configs)

class ImplicitKey(Getter):

    def __init__(self, wrapped_config, key):
        super().__init__()
        self.key = key
        self.wrapped_config = wrapped_config

    def __reprargs__(self):
        return [repr(self.wrapped_config), repr(self.key)]

    def bind(self, obj, param):
        return BoundKey(self, obj, param, [self.wrapped_config])

class Func(Getter):

    def __init__(self, callable, *, skip=(), dynamic=False, **kwargs):
        super().__init__(**kwargs)
        self.callable = callable
        self.skip = skip
        self.dynamic = dynamic
        self.partial_args = ()
        self.partial_kwargs = {}

    def __reprargs__(self):
        return [repr(self.callable)]

    def partial(self, *args, **kwargs):
        self.partial_args = args
        self.partial_kwargs = kwargs
        return self

    def bind(self, obj, param):
        return BoundCallable(
                self, obj, param,
                self.callable,
                self.partial_args,
                self.partial_kwargs,
                self.dynamic,
                tuple(always_iterable(self.skip)),
        )

class Method(Func):

    def __init__(self, *args, dynamic=True, **kwargs):
        super().__init__(*args, dynamic=dynamic, **kwargs)

    def bind(self, obj, param):
        # Methods used with this getter this will typically attempt to 
        # calculate a value based on other BYOC-managed attributes.  In most 
        # cases, a `NoValueFound` exception will be raised if any of those 
        # attributes is missing a value.  The most sensible thing to do when 
        # this happens is to silently skip this getter, allowing the parameter 
        # that invoked it to continue searching other getters for a value.

        bc = super().bind(obj, param)
        bc.partial_args = (obj, *bc.partial_args)
        bc.exceptions = bc.exceptions or (NoValueFound,)
        return bc

class Attr(Getter):

    def __init__(self, attr, *, skip=(), dynamic=False, **kwargs):
        super().__init__(**kwargs)
        self.attr = attr
        self.skip = skip
        self.dynamic = dynamic

    def __reprargs__(self):
        return [repr(self.attr)]

    def bind(self, obj, param):
        return BoundAttr(
                self, obj, param, self.attr,
                exc=self.skip or (NoValueFound,),
                dynamic=self.dynamic,
        )

class Value(Getter):

    def __init__(self, value, **kwargs):
        super().__init__(**kwargs)
        self.value = value

    def __reprargs__(self):
        return [repr(self.value)]

    def bind(self, obj, param):
        return BoundValue(self, obj, param, self.value)



class BoundGetter:

    def __init__(self, parent, obj, param):
        self.parent = parent
        self.obj = obj
        self.param = param

        # The following attributes are public and may be accessed or modified 
        # by `param` subclasses (e.g. `toggle_param`).  Be careful when making 
        # modifications, though, because any modifications will need to be 
        # re-applied each time the cache expires (because the getters are 
        # re-bound when this happens).
        self.kwargs = parent.kwargs
        self.cast_funcs = list(value_chain(
            self.kwargs.get('cast', []),
            param._get_default_cast()
        ))

        self._check_kwargs()

    def _check_kwargs(self):
        given_kwargs = set(self.kwargs.keys())
        known_kwargs = self.param._get_known_getter_kwargs()
        unknown_kwargs = given_kwargs - known_kwargs

        if unknown_kwargs:
            err = ApiError(
                    getter=self.parent,
                    obj=self.obj,
                    param=self.param,
                    given_kwargs=given_kwargs,
                    known_kwargs=known_kwargs,
                    unknown_kwargs=unknown_kwargs,
            )
            err.brief = f'unexpected keyword argument'
            err.info += lambda e: '\n'.join([
                f"{e.param.__class__.__name__}() allows the following kwargs:",
                *e.known_kwargs,
            ])
            err.blame += lambda e: '\n'.join([
                f"{e.getter!r} has the following unexpected kwargs:",
                *e.unknown_kwargs,
            ])
            raise err

    def iter_values(self, log):
        raise NotImplementedError

    def cast_value(self, value, meta):
        for f in self.cast_funcs:
            context = Context(value, meta, self.obj)
            value = call_with_context(f, context)
        return value

class BoundKey(BoundGetter):

    def __init__(self, parent, obj, param, wrapped_configs):
        super().__init__(parent, obj, param)
        self.key = parent.key
        self.wrapped_configs = wrapped_configs

        if self.key is UNSPECIFIED:
            self.key = param._get_default_key()

    def iter_values(self, log):
        assert self.key is not UNSPECIFIED
        assert self.wrapped_configs is not None

        if not self.wrapped_configs:
            log += f"no configs of class {self.parent.config_cls.__name__}"

        for wrapped_config in self.wrapped_configs:
            config = wrapped_config.config

            if not wrapped_config.is_loaded:
                log += f"skipped {config}: not loaded"
                log += "did you mean to call `byoc.load()`?"
                continue

            if not wrapped_config.layers:
                # If a config has no layers, that probably means an error 
                # occurred when the config was being loaded.  Most likely, the 
                # cause of this error was that some attribute of the object 
                # either wasn't defined, or didn't have an appropriate value.  
                # If the attribute in question was given an appropriate value 
                # after the config was loaded, the config will need to be 
                # reloaded before that value takes effect.
                #
                # That said, I decided to only include a literal description of 
                # the error here, and to leave it to the configs to suggest how 
                # to fix the problem, e.g. by calling `reload()`.  The reason 
                # is that I think a generic message would be wrong/confusing in 
                # too many cases.
                log += f"skipped {config}: loaded, but no layers"
                config.load_status(log)
                continue

            log += f"queried {config}:"
            config.load_status(log)

            for layer in wrapped_config:
                for value in layer.iter_values(self.key, log):
                    yield (
                            value,
                            LayerMeta(self.parent, layer),
                            config.dynamic,
                    )

class BoundCallable(BoundGetter):

    def __init__(self, parent, obj, param, callable, args, kwargs, dynamic, exc=()):
        super().__init__(parent, obj, param)
        self.callable = callable
        self.partial_args = args
        self.partial_kwargs = kwargs
        self.dynamic = dynamic
        self.exceptions = exc

    def iter_values(self, log):
        try:
            value = self.callable(*self.partial_args, **self.partial_kwargs)
        except self.exceptions as err:
            log += f"called: {self.callable}\nraised {err.__class__.__name__}: {err}"
        else:
            log += lambda: f"called: {self.callable}\nreturned: {value!r}"
            yield value, GetterMeta(self.parent), self.dynamic

class BoundAttr(BoundGetter):

    def __init__(self, parent, obj, param, attr, dynamic, exc=()):
        super().__init__(parent, obj, param)
        self.attr = attr
        self.dynamic = dynamic
        self.exceptions = exc

    def iter_values(self, log):
        qualattr = f'{self.obj.__class__.__name__}.{self.attr}'
        try:
            value = getattr(self.obj, self.attr)
        except self.exceptions as err:
            log += f"looked up: {qualattr}\nraised {err.__class__.__name__}: {err}"
        else:
            log += f"looked up: {qualattr}\nreturned: {value!r}"
            yield value, GetterMeta(self.parent), self.dynamic

class BoundValue(BoundGetter):

    def __init__(self, parent, obj, param, value):
        super().__init__(parent, obj, param)
        self.value = value

    def iter_values(self, log):
        log += lambda: f"got hard-coded value: {self.value!r}"
        yield self.value, GetterMeta(self.parent), False






