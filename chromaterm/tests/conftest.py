'''pytest configuration'''
import os
from ctypes.util import find_library

# Color-related variables leak from the outer environment into the tests and
# the ChromaTerm subprocesses they spawn, changing the expected behavior (e.g.
# `NO_COLOR` disables highlighting entirely). Remove them so the tests are
# hermetic regardless of the environment they run in.
for variable in ('NO_COLOR', 'CT_NO_COLOR', 'FORCE_COLOR', 'COLORTERM',
                 'TERM_PROGRAM', 'VTE_VERSION', 'WT_SESSION'):
    os.environ.pop(variable, None)


def pytest_generate_tests(metafunc):
    '''Run tests with the `pcre` fixture twice; Once with `pcre=False`, another
    time with `pcre=True` if the library is present.'''
    if find_library('pcre2-8') and 'pcre' in metafunc.fixturenames:
        metafunc.parametrize('pcre', [False, True])
