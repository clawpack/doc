"""
Tests for tools/check_doc_env.py.

Runnable either directly (``python tools/test_check_doc_env.py``) or under
pytest.  They build the import failures synthetically -- a module object with
an empty ``__path__``, a temporary directory standing in for ``$CLAW`` -- so
they need neither a Clawpack checkout nor the doc toolchain.

What they protect: `checkenv` has to say *which* of three unrelated problems
it hit.  A maintainer once got the "pin the dependency or mock it" advice for
a stale geoclaw checkout and a file missing from riemann's meson.build, which
is the remedy for neither, and the misdirection cost more than the bugs.
"""

import os
import sys
import tempfile
import types

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# The module reads $CLAW at import time, so fix it to a known root first.
FAKE_CLAW = tempfile.mkdtemp(prefix='fake-claw-')
os.environ['CLAW'] = FAKE_CLAW

import check_doc_env as cde  # noqa: E402


def _from_import_error(package, attribute):
    """The ImportError raised by ``from . import <attribute>``.

    This is riemann's shape: ``clawpack.riemann.acoustics_1D_py`` is the
    target that fails, while ``euler_mapgrid_3D_constants`` -- imported by the
    package's __init__ -- is what is actually missing.
    """
    module = types.ModuleType(package)
    module.__path__ = []
    sys.modules[package] = module
    try:
        exec(f'from . import {attribute}',
             {'__name__': package, '__package__': package})
    except ImportError as exc:
        return exc
    finally:
        del sys.modules[package]
    raise AssertionError('expected an ImportError')


def _module_not_found(name):
    try:
        __import__(name)
    except ImportError as exc:
        return exc
    raise AssertionError(f'expected {name} to be absent')


def _fake_clawpack(*subdirs):
    """Install a stand-in ``clawpack`` whose __path__ points into $CLAW."""
    module = types.ModuleType('clawpack')
    module.__path__ = [os.path.join(FAKE_CLAW, *d.split('/')) for d in subdirs]
    for path in module.__path__:
        os.makedirs(path, exist_ok=True)
    sys.modules['clawpack'] = module
    return module


def test_missing_name_from_module_not_found():
    """The stale-checkout shape: `No module named 'clawpack.geoclaw.met'`."""
    exc = _module_not_found('clawpack_absent_pkg_for_test')
    assert cde._missing_name(exc) == 'clawpack_absent_pkg_for_test'


def test_missing_name_from_a_failed_from_import():
    """The riemann shape, where exc.name is only half the answer."""
    exc = _from_import_error('clawpack_fake_riemann', 'euler_mapgrid_3D_constants')
    assert cde._missing_name(exc) == (
        'clawpack_fake_riemann.euler_mapgrid_3D_constants')


def test_missing_name_falls_back_to_the_message():
    """Older interpreters set neither name nor name_from."""
    bare = ImportError("cannot import name 'gone' from 'clawpack.riemann'")
    assert cde._missing_name(bare) == 'clawpack.riemann.gone'
    bare = ImportError("No module named 'clawpack.geoclaw.met'")
    assert cde._missing_name(bare) == 'clawpack.geoclaw.met'


def test_missing_name_gives_up_quietly():
    assert cde._missing_name(ImportError('something else entirely')) is None


def test_source_path_resolves_under_a_broken_parent():
    """riemann again: the parent package is exactly what failed to import.

    _source_path must fall back to clawpack's own __path__ and still find the
    file, or the "it is right here on disk" diagnosis is impossible.
    """
    _fake_clawpack('riemann', 'geoclaw/src/python')
    target = os.path.join(FAKE_CLAW, 'riemann', 'riemann')
    os.makedirs(target, exist_ok=True)
    expected = os.path.join(target, 'euler_mapgrid_3D_constants.py')
    open(expected, 'w').close()

    path, searched = cde._source_path(
        'clawpack.riemann.euler_mapgrid_3D_constants')
    assert path == expected
    assert searched, 'the searched-paths list is what the report prints'


def test_source_path_reports_absence_and_where_it_looked():
    """The stale-checkout case: nothing on disk, and the paths tried."""
    _fake_clawpack('geoclaw/src/python')
    path, searched = cde._source_path('clawpack.geoclaw.met.gridded')
    assert path is None
    assert any(p.endswith(os.path.join('geoclaw', 'met', 'gridded.py'))
               for p in searched), searched


def test_classify_absent_module():
    _fake_clawpack('geoclaw/src/python')
    kind, missing, searched = cde.classify(
        ImportError("No module named 'clawpack.geoclaw.met'"))
    assert kind == 'absent'
    assert missing == 'clawpack.geoclaw.met'
    assert isinstance(searched, list)


def test_classify_on_disk_but_unexposed():
    """The install-shadows-the-tree case, which needs its own remedy."""
    _fake_clawpack('riemann')
    target = os.path.join(FAKE_CLAW, 'riemann', 'riemann')
    os.makedirs(target, exist_ok=True)
    open(os.path.join(target, 'static.py'), 'w').close()

    kind, missing, path = cde.classify(
        ImportError("cannot import name 'static' from 'clawpack.riemann'"))
    assert kind == 'unexposed'
    assert missing == 'clawpack.riemann.static'
    assert path.endswith(os.path.join('riemann', 'riemann', 'static.py'))


def test_classify_third_party():
    kind, missing, _ = cde.classify(
        ImportError("No module named 'petsc4py'"))
    assert kind == 'third_party'
    assert missing == 'petsc4py'


def test_classify_attribute_error_is_not_a_missing_module():
    """AttributeError also has a `.name`, and it is not a module name."""
    kind, missing, _ = cde.classify(
        AttributeError("module 'clawpack.geoclaw.topotools' has no attribute "
                       "'Topography2'", name='Topography2'))
    assert kind == 'attribute'
    assert missing == 'Topography2'


def test_classify_gives_up_out_loud():
    kind, missing, _ = cde.classify(ValueError('not an import problem'))
    assert kind == 'unknown'
    assert missing is None


def test_shadowing_install_detects_a_mesonpy_finder():
    """The one fact that explains "the file is there but will not import"."""
    class MesonpyMetaFinder:
        pass

    sys.meta_path.insert(0, MesonpyMetaFinder())
    try:
        install = cde._shadowing_install()
    finally:
        sys.meta_path.pop(0)
    assert install is not None
    version, finders = install
    assert any('meson-python' in f for f in finders), finders


if __name__ == '__main__':
    failures = 0
    for name, func in sorted(globals().items()):
        if name.startswith('test_') and callable(func):
            try:
                func()
            except AssertionError as exc:
                failures += 1
                print(f'FAIL {name}: {exc}')
            else:
                print(f'ok   {name}')
    sys.exit(1 if failures else 0)
