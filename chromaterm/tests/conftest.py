'''pytest configuration'''
from ctypes.util import find_library

import pytest


def pytest_generate_tests(metafunc):
    '''Run tests with the `pcre` fixture twice; Once with `pcre=False`, another
    time with `pcre=True` if the library is present.'''
    if find_library('pcre2-8') and 'pcre' in metafunc.fixturenames:
        metafunc.parametrize('pcre', [False, True])


@pytest.fixture(autouse=True)
def _force_color_output(monkeypatch):
    '''Ensure CLI tests are not impacted by ambient NO_COLOR settings.'''
    monkeypatch.delenv('NO_COLOR', raising=False)
    monkeypatch.delenv('CT_NO_COLOR', raising=False)
