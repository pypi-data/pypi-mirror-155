#!/usr/bin/env python3

import byoc
import pytest
import sys

from parametrize_from_file import Namespace, cast, defaults, error_or
from voluptuous import Schema, And, Or, Optional, Invalid, Coerce
from unittest.mock import Mock
from re_assert import Matches
from pathlib import Path

if sys.version_info[:2] >= (3, 10):
    from functools import partial
    zip_equal = partial(zip, strict=True)
else:
    from more_itertools import zip_equal

with_py = Namespace('from operator import itemgetter', Mock=Mock)
with_byoc = Namespace(byoc, 'from byoc import *', list=list)

class LayerWrapper:

    def __init__(self, layer):
        self.layer = layer

    def __repr__(self):
        return f'LayerWrapper({self.layer!r})'

    def __eq__(self, other):
        def str_or_none(x):
            return str(x) if x is not None else x

        if not isinstance(other, byoc.Layer):
            print('not a layer')
            return False

        if type(self.layer) != type(other):
            print('wrong layer type')
            return False

        if hasattr(self.layer, 'values'):
            if self.layer.values != other.values:
                print('wrong layer values')
                return False

        if hasattr(self.layer, 'location'):
            if str_or_none(self.layer.location) != str_or_none(other.location):
                print('wrong layer location')
                return False

        if hasattr(self.layer, 'root_key'):
            if self.layer.root_key != other.root_key:
                print('wrong layer root key')
                return False

        if hasattr(self.layer, 'schema'):
            if self.layer.schema != other.schema:
                print('wrong layer schema')
                return False

        if hasattr(self.layer, 'linenos'):
            other_linenos = {k: v.line.lineno for k, v in other.linenos.items()}
            if self.layer.linenos != other_linenos:
                print('wrong layer linenos')
                return False

        return True

class DictLayerWrapper(LayerWrapper):

    def __init__(self, *args, **kwargs):
        super().__init__(byoc.DictLayer(*args, **kwargs))

class MetaWrapper:

    def __init__(self, type, location=None, **kwargs):
        self.type = type
        self.location = location
        self.kwargs = kwargs

    def __repr__(self):
        kwargs = {
                'location': self.location,
                **self.kwargs,
        }
        if not self.location:
            del kwargs['location']

        type_str = self.type.__name__
        kwargs_strs = [
                f'{k}={v!r}'
                for k, v in kwargs.items()
        ]

        return f'{self.__class__.__name__}({", ".join([type_str, *kwargs_strs])})'

    def __eq__(self, other):
        if not isinstance(other, self.type):
            print('wrong meta type')
            return False

        if self.location != other.location:
            print('wrong meta location')
            return False

        try:
            getter_cls = self.kwargs['getter']
        except KeyError:
            pass
        else:
            if not isinstance(other.getter, getter_cls):
                print('wrong meta getter')
                return False

        try:
            value = self.kwargs['getter.value']
        except KeyError:
            pass
        else:
            if other.getter.value != value:
                print('wrong meta getter value')
                return False

        try:
            values = self.kwargs['layer.values']
        except KeyError:
            pass
        else:
            if other.layer.values != values:
                print('wrong meta layer values')
                return False

        return True

def eval_obj_layers(layers):
    schema = Schema(empty_ok({
        Coerce(int): eval_config_layers,
    }))
    return schema(layers)

def eval_config_layers(layers):
    schema = Schema(empty_ok([eval_layer]))
    return schema(layers)

def eval_layer(layer):
    schema = Schema(Or(str, {
        'values': with_py.eval,
        'location': str,
        Optional('root_key'): with_py.eval,
        Optional('schema'): with_py.eval,
        Optional('linenos'): with_py.eval,
    }))
    layer = schema(layer)
    layer = with_byoc.eval(layer) if isinstance(layer, str) else \
            byoc.DictLayer(**layer)
    return LayerWrapper(layer)

def eval_meta(meta):
    with_meta = Namespace(
            with_byoc,
            'from byoc.meta import *',
            MetaWrapper=MetaWrapper,
    )
    dict_schema = {
            'type': with_meta.eval,
            Optional('location', default=None): Or(None, str),
            str: with_byoc.eval,
    }
    schema = Schema(Or(dict_schema, with_meta.eval))
    meta = schema(meta)

    if isinstance(meta, MetaWrapper):
        return meta
    elif isinstance(meta, dict):
        return MetaWrapper(**meta)
    else:
        return MetaWrapper(meta)

def collect_layers(obj):
    wrapped_configs = byoc.model.get_wrapped_configs(obj)
    return {
            i: wc.layers
            for i, wc in enumerate(wrapped_configs)
    }

def assert_log_matches(log, expected):
    for log_str, pattern in zip_equal(log.message_strs, expected):
        Matches(pattern).assert_matches(log_str)

def find_param(obj, name=None):
    from more_itertools import only
    class_attrs = obj.__class__.__dict__

    if name:
        return class_attrs[name]
    else:
        params = (
                x for x in class_attrs.values()
                if isinstance(x, byoc.param)
        )
        default = byoc.param()
        default.__set_name__(obj.__class__, '')
        return only(params, default)

def get_obj_or_cls(obj_name, cls_name=None):
    if not cls_name:
        cls_name = f'Dummy{obj_name.title()}'

    def get(ns):
        try:
            return ns[obj_name]
        except KeyError:
            return ns[cls_name]()

    return get

def empty_ok(container):
    return Or(container, And('', lambda y: type(container)()))

get_obj = get_obj_or_cls('obj')
get_config = get_obj_or_cls('config')
get_meta = get_obj_or_cls('meta')
no_templates = '^[^{}]*$'

@pytest.fixture
def files(request, tmp_path):

    # We want to return a `pathlib.Path` instance with an extra `manifest` 
    # attribute that records the specific file names/contents the were 
    # provided.  Unfortunately, `pathlib.Path` uses slots, so the only way to 
    # do this is to make our own subclass.  This is complicated further by the 
    # fact that `pathlib.Path` is just a factory, and instantiates different 
    # classes of objects depending on the operating system.

    class TestPath(type(tmp_path)):
        __slots__ = ('manifest',)

    tmp_path = TestPath._from_parts([tmp_path])
    tmp_path.manifest = request.param

    for name, contents in request.param.items():
        p = tmp_path / name
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(contents)

    return tmp_path

files.schema = empty_ok({str: str})
