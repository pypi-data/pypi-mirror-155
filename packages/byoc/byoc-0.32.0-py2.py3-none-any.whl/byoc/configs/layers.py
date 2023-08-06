#!/usr/bin/env python3

import functools, os
from inspect import isclass
from ..utils import lookup

class Layer:

    def iter_values(self, key, log):
        raise NotImplementedError

class DictLayer(Layer):

    def __init__(self, values, *, schema=None, root_key=None, location=None, linenos=None):
        # Values:
        # - object that implements `__getitem__()` to either return value 
        #   associated with key, or raise KeyError.
        # - callable that takes no arguments and returns an object matching the 
        #   above description.
        #
        # Location:
        # - string
        # - callable that takes no arguments and returns a string.
        self.values = values
        self.linenos = linenos or {}
        self.schema = schema
        self.root_key = root_key
        self.location = location

    def __repr__(self):
        attrs = {
                'schema': self.schema,
                'root_key': self.root_key,
                'location': self.location,
        }
        attr_strs = [f'{k}={v!r}' for k, v in attrs.items() if v]
        attrs_str = ', '.join([repr(self.values), *attr_strs])
        return f'{self.__class__.__name__}({attrs_str})'

    def iter_values(self, key, log):
        values = self.values

        if self.root_key:
            try:
                values = lookup(values, self.root_key)
            except KeyError:
                log += lambda: format_loc(
                        f"did not find {self.root_key!r} in {repr_dict_short(values)}",
                        self.location,
                )
                return

        if self.schema:
            values = self.schema(values)

        try:
            value = lookup(values, key)
        except KeyError:
            log += lambda: format_loc(
                    f"did not find {key!r} in {repr_dict_short(values)}",
                    self.location,
            )
        else:
            log += lambda: format_loc(
                    f"called: {key!r}\nreturned: {value!r}" if callable(key) else
                    f"found {key!r}: {value!r}",
                    self.location,
            )
            yield value

    @property
    def values(self):
        if self._are_values_deferred:
            self._values = self._values()
            self._are_values_deferred = False
        return self._values

    @values.setter
    def values(self, values):
        self._values = values
        self._are_values_deferred = callable(values)

    @property
    def location(self):
        if self._is_location_deferred:
            self._location = self._location()
            self._is_location_deferred = False
        return self._location

    @location.setter
    def location(self, loc):
        self._location = loc
        self._is_location_deferred = callable(loc)

class FileNotFoundLayer(Layer):

    def __init__(self, path):
        self.location = path

    def iter_values(self, key, log):
        log += f"file does not exist: {self.location}\ndid not find {key!r}"
        return
        yield  # pragma: no cover


def dict_like(*args):

    # I want this function to be usable as a decorator, but I also want to 
    # avoid exposing `__call__()` so that these objects don't look like 
    # deferred values to `Layer`.  These competing requirements necessitate an 
    # awkward layering of wrapper functions and classes.
    
    class dict_like:

        def __init__(self, f, *raises):
            self.f = f
            self.raises = raises

        def __repr__(self):
            return f"{self.__class__.__name__}({self.f!r})"

        def __getitem__(self, key):
            try:
                return self.f(key)
            except tuple(self.raises) as err:
                raise KeyError from err

    is_exception = lambda x: isclass(x) and issubclass(x, Exception)

    if not args:
        return lambda f: dict_like(f)

    elif is_exception(args[0]):
        return lambda f: dict_like(f, *args)

    else:
        return dict_like(*args)

def format_loc(message, loc):
    prefix = f"{loc}:\n" if loc else ""
    return prefix + message

def repr_dict_short(d):
    import sys
    from collections.abc import Mapping
    from textwrap import shorten
    from pprint import pformat

    # Since this function is used for logging, we don't want to crash on 
    # unexpected input.  So we check if the given object is actually a mapping, 
    # and if it's not, we pass it to `pformat()`, which will just use its repr.

    if os.environ.get('BYOC_VERBOSE') or not isinstance(d, Mapping):
        return pformat(d, depth=1, compact=True, width=sys.maxsize)

    try:
        n_max = int(os.environ['BYOC_DICT_KEY_LIMIT'])
    except (KeyError, ValueError):
        n_max = 20

    if len(d) <= n_max:
        key_strs = [f'{k!r}: …' for k in d]
    else:
        n = n_max // 2
        key_strs = [f'{k!r}: …' for k in list(d)[:n]]
        key_strs.append(f'and {len(d) - n} others')

    dict_str = '{' + ', '.join(key_strs) + '}'
    return f'{dict_str}\nTo see the whole dictionary, set the following environment variable: BYOC_VERBOSE=1'
