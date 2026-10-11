"""
Tests for tools/check_doc_warnings.py.

Runnable either directly (``python tools/test_check_doc_warnings.py``) or under
pytest.  These feed synthetic Sphinx warning lines through the signature
normaliser rather than running Sphinx, so they are fast and need none of the
doc toolchain.

What they protect: a warning signature has to mean the same thing on a
developer's laptop and on a CI runner, or the committed baseline silently
becomes a list of one machine's warnings.  The real failures that motivated
each case are named in the individual tests.
"""

import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# The module reads $CLAW at import time, so fix it to a known root first.
FAKE_CLAW = '/fake/claw'
os.environ['CLAW'] = FAKE_CLAW

import check_doc_warnings as cdw  # noqa: E402


def signature(line):
    """The signature check_doc_warnings would record for a raw warning line."""
    match = cdw._WARNING_RE.match(line)
    assert match is not None, f'no warning matched in {line!r}'
    return cdw._signature(match)


def test_rst_location_is_relative_to_claw():
    assert signature(
        f'{FAKE_CLAW}/doc/doc/topo.rst:123: WARNING: undefined label: x'
    ) == 'doc/doc/topo.rst: WARNING: undefined label: x'


def test_doc_paths_do_not_depend_on_where_claw_points():
    """$CLAW can be a pinned tree far away from the doc repository.

    Both spellings of the same .rst file -- inside $CLAW (the default layout)
    and inside this repository (the pinned-tree layout) -- must produce one
    signature, or switching to `make claw-pin` would rewrite the baseline.
    """
    inside_claw = signature(
        f'{FAKE_CLAW}/doc/doc/topo.rst:1: WARNING: undefined label: x')
    in_repo = signature(
        f'{cdw.SRC_DIR}/topo.rst:1: WARNING: undefined label: x')
    assert inside_claw == in_repo == 'doc/doc/topo.rst: WARNING: undefined label: x'


def test_line_numbers_are_dropped():
    """Editing a file above a warning must not churn the baseline."""
    a = signature(f'{FAKE_CLAW}/doc/doc/topo.rst:12: WARNING: undefined label: x')
    b = signature(f'{FAKE_CLAW}/doc/doc/topo.rst:900: WARNING: undefined label: x')
    assert a == b


def test_docstring_location_drops_the_file():
    """The same docstring warning, from a source tree and from site-packages.

    Where the module file lives depends only on how clawpack was made
    importable; the dotted name is the same object either way.
    """
    from_source = signature(
        f'{FAKE_CLAW}/geoclaw/src/python/geoclaw/util.py:docstring of '
        'clawpack.geoclaw.util.bearing:7: ERROR: Unexpected indentation.')
    from_install = signature(
        '/opt/hostedtoolcache/Python/3.12.14/x64/lib/python3.12/site-packages/'
        'clawpack/geoclaw/util.py:docstring of '
        'clawpack.geoclaw.util.bearing:7: ERROR: Unexpected indentation.')
    assert from_source == from_install
    assert from_source == ('docstring of clawpack.geoclaw.util.bearing: '
                           'ERROR: Unexpected indentation.')


def test_absolute_paths_inside_messages_are_scrubbed():
    """The failure that produced two spurious "new" warnings on every CI run.

    Sphinx names the other end of a duplicate-label conflict by absolute path,
    which _normalize_location never saw because it is in the message.
    """
    local = signature(
        f'{FAKE_CLAW}/doc/doc/pyclaw/about.rst:4: WARNING: duplicate label '
        f'about, other instance in {FAKE_CLAW}/doc/doc/about.rst')
    assert local == ('doc/doc/pyclaw/about.rst: WARNING: duplicate label '
                     'about, other instance in doc/doc/about.rst')
    assert FAKE_CLAW not in local


def test_message_paths_outside_claw_are_left_alone():
    """Scrubbing must not mangle paths that are part of the message's meaning."""
    sig = signature('WARNING: image file not readable: /etc/nonexistent.png')
    assert '/etc/nonexistent.png' in sig


def test_locationless_warnings_keep_their_shape():
    assert signature(
        "WARNING: A mocked object is detected: 'clawpack.petclaw.state.State' "
        '[autodoc.mocked_object]'
    ).startswith('WARNING: A mocked object is detected:')


def test_autodoc_import_failures_are_always_fatal():
    sig = ("WARNING: autodoc: failed to import module 'topotools' from module "
           "'clawpack.geoclaw'; the following exception was raised:")
    assert cdw._always_fail(sig) is not None
    assert cdw._always_fail('doc/doc/topo.rst: WARNING: undefined label: x') is None


def test_update_refuses_to_record_always_fail_warnings():
    """--update must not be able to bless an environment failure into silence."""
    keep = 'doc/doc/topo.rst: WARNING: undefined label: x'
    drop = ("WARNING: autodoc: failed to import module 'topotools' from "
            "module 'clawpack.geoclaw'; the following exception was raised:")

    with tempfile.TemporaryDirectory() as tmp:
        original = cdw.BASELINE
        cdw.BASELINE = os.path.join(tmp, 'baseline.txt')
        try:
            cdw.write_baseline({keep, drop})
            written = cdw.load_baseline()
        finally:
            cdw.BASELINE = original

    assert keep in written
    assert drop not in written


def main():
    tests = [v for k, v in sorted(globals().items()) if k.startswith('test_')]
    for test in tests:
        test()
        print(f'ok   {test.__name__}')
    print(f'\n{len(tests)} test(s) passed.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
