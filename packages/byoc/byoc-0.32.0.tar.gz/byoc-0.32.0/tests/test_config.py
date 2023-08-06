#!/usr/bin/env python3

import byoc
import pytest
import parametrize_from_file
import sys, os, shlex, re

from byoc.errors import Log
from pytest_unordered import unordered
from unittest import mock
from pathlib import Path
from param_helpers import *

@pytest.fixture
def tmp_chdir(tmp_path):
    import os
    try:
        cwd = os.getcwd()
        os.chdir(tmp_path)
        yield tmp_path
    finally:
        os.chdir(cwd)


@parametrize_from_file(
        schema=[
            cast(
                factory=with_byoc.exec(get='DummyConfig', defer=True),
                expected=with_py.eval,
            ),
            with_byoc.error_or('expected')
        ],
)
def test_config_init(factory, expected, error):
    class DummyObj:
        pass

    factory = factory()
    obj = DummyObj()

    with error:
        config = factory(obj)

        for attr, value in expected.items():
            assert getattr(config, attr) == value

@parametrize_from_file(
        schema=cast(
            obj=with_byoc.exec(get=get_obj),
            invocations=Schema([{
                'argv': shlex.split,
                'expected': {str: with_py.eval},
            }]),
        ),
)
def test_argparse_docopt_config(monkeypatch, obj, usage, brief, invocations):
    from copy import copy

    for invocation in invocations:
        print(invocation)

        test_obj = copy(obj)
        test_argv = invocation['argv']
        test_expected = invocation['expected']

        # Clear `sys.argv` so that if the command-line is accessed prematurely, 
        # e.g. in `init()` rather than `load()`, an error is raised.  Note that 
        # `sys.argv[0]` needs to be present, because `argparse` checks this 
        # when generating usage text.
        monkeypatch.setattr(sys, 'argv', ['app'])

        # These attributes should be available even before `init()` is called.  
        # Note that accessing these attributes may trigger `init()`, e.g. if 
        # the usage text contains default values based on BYOC-managed 
        # attributes.
        if sys.version_info[:2] >= (3, 10):
            usage = re.sub('(?m)^optional arguments:$', 'options:', usage)

        assert test_obj.usage == usage
        assert test_obj.brief == brief

        # Make sure that calling `init()` (if it wasn't implicitly called 
        # above) doesn't cause the command line to be read.
        byoc.init(test_obj)

        monkeypatch.setattr(sys, 'argv', test_argv)
        byoc.load(test_obj)

        for attr, value in test_expected.items():
            assert getattr(test_obj, attr) == value

@mock.patch.dict(os.environ, {"x": "1"})
def test_environment_config():
    class DummyObj:
        __config__ = [byoc.EnvironmentConfig]
        x = byoc.param()

    obj = DummyObj()
    assert obj.x == "1"

@parametrize_from_file(
        schema=cast(
            obj=with_byoc.exec(get=get_obj),
            slug=with_py.eval,
            author=with_py.eval,
            version=with_py.eval,
            files=Schema(files.schema),
            layers=eval_config_layers,
        ),
        indirect=['files'],
)
def test_appdirs_config(tmp_chdir, monkeypatch, obj, slug, author, version, files, layers):
    import appdirs

    class AppDirs:

        def __init__(self, slug, author, version):
            self.slug = slug
            self.author = author
            self.version = version

            self.user_config_dir = 'user'
            self.site_config_dir = 'site'

    monkeypatch.setattr(appdirs, 'AppDirs', AppDirs)

    assert obj.dirs.slug == slug
    assert obj.dirs.author == author
    assert obj.dirs.version == version
    assert list(obj.config_paths) == unordered([
        Path(x)
        for x in files.manifest.keys()
    ])

    byoc.init(obj)
    assert collect_layers(obj)[0] == layers

@parametrize_from_file(
        schema=[
            cast(
                config=with_byoc.eval(defer=True),
                config_cls=with_byoc.eval
            ),
            with_byoc.error_or('name', 'config_cls'),
        ],
)
def test_appdirs_config_get_name_and_config_cls(config, name, config_cls, error):
    config = config()(Mock())

    with error:
        actual_name, actual_config_cls = config.get_name_and_config_cls()
        assert actual_name == name
        assert actual_config_cls == config_cls

@parametrize_from_file(
        schema=[
            cast(
                obj=with_byoc.exec(get=get_obj),
                files=Schema(files.schema),
                layers=eval_config_layers,
            ),
            defaults(load_status=[]),
        ],
        indirect=['files'],
)
def test_file_config(tmp_chdir, obj, files, layers, load_status):
    byoc.init(obj)
    assert collect_layers(obj)[0] == layers

    log = log_load_status(obj)
    assert_log_matches(log, load_status)

def test_file_config_load_status():

    class DummyObj:
        __config__ = [byoc.YamlConfig]
        x = byoc.param()

    obj = DummyObj()

    with pytest.raises(byoc.NoValueFound) as err:
        obj.x

    assert err.match(r"failed to get path\(s\):")
    assert err.match(r"raised AttributeError: 'DummyObj' object has no attribute 'path'")

@parametrize_from_file
def test_on_load(prepare, load, expected):

    class DummyConfig(byoc.Config):
        def load(self):
            yield byoc.DictLayer(values={})

    class A(DummyConfig):
        pass

    class A1(A):
        pass

    class A2(A):
        pass

    class B(DummyConfig):
        autoload = False

    class B1(B):
        pass

    class B2(B):
        pass

    class DummyObj:
        __config__ = [A1, A2, B1, B2]

        def __init__(self):
            self.calls = set()

        @byoc.on_load
        def on_default(self):
            self.calls.add('default')

        @byoc.on_load(DummyConfig)
        def on_dummy_config(self):
            self.calls.add('DummyConfig')

        @byoc.on_load(A)
        def on_a(self):
            self.calls.add('A')

        @byoc.on_load(A1)
        def on_a1(self):
            self.calls.add('A1')

        @byoc.on_load(A2)
        def on_a2(self):
            self.calls.add('A2')

        @byoc.on_load(B)
        def on_b(self):
            self.calls.add('B')

        @byoc.on_load(B1)
        def on_b1(self):
            self.calls.add('B1')

        @byoc.on_load(B2)
        def on_b2(self):
            self.calls.add('B2')

    obj = DummyObj()

    with_locals = Namespace(with_byoc, locals())
    with_locals.exec(prepare)

    obj.calls = set()

    with_locals.exec(load)
    assert obj.calls == set(expected or [])

def test_on_load_inheritance():

    class DummyConfig(byoc.Config):
        def load(self):
            yield byoc.DictLayer(values={})

    class P:
        __config__ = [DummyConfig]

        def __init__(self):
            self.calls = set()

        @byoc.on_load
        def a(self):
            self.calls.add('P/a')

        @byoc.on_load
        def b(self):
            self.calls.add('P/b')

        @byoc.on_load
        def c(self):
            self.calls.add('P/c')

    class F1(P):

        @byoc.on_load
        def a(self):
            self.calls.add('F1/a')

        @byoc.on_load
        def b(self):
            self.calls.add('F1/b')

    class F2(F1):

        @byoc.on_load
        def a(self):
            self.calls.add('F2/a')

    p = P()
    f1 = F1()
    f2 = F2()

    byoc.init(p)
    byoc.init(f1)
    byoc.init(f2)

    assert p.calls  == { 'P/a',  'P/b', 'P/c'}
    assert f1.calls == {'F1/a', 'F1/b', 'P/c'}
    assert f2.calls == {'F2/a', 'F1/b', 'P/c'}

@parametrize_from_file(
        schema=[
            cast(
                f=with_byoc.exec(get='f'),
                raises=with_py.eval,
                x=with_py.eval,
                expected=with_py.eval,
            ),
            defaults(raises=[]),
            error_or('x', 'expected'),
        ],
)
@pytest.mark.parametrize(
        'factory', [
            pytest.param(
                lambda f, raises: byoc.dict_like(*raises)(f),
                id='decorator',
            ),
            pytest.param(
                lambda f, raises: byoc.dict_like(f, *raises),
                id='constructor',
            ),
        ]
)
def test_dict_like(factory, f, raises, x, expected, error):
    with error:
        g = factory(f, raises)
        assert g[x] == expected

def test_dict_like_repr():
    d = byoc.dict_like(int)
    assert repr(d) == "dict_like(<class 'int'>)"


def log_load_status(obj):
    log = Log()

    for wc in byoc.model.get_wrapped_configs(obj):
        wc.config.load_status(log)

    return log

