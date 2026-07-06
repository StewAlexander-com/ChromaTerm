'''Platform-specific helpers used by ChromaTerm.'''
from __future__ import annotations

import os
import signal
import sys
from typing import Callable, Optional, Union

IS_WINDOWS = sys.platform == 'win32'
SUPPORTS_PTY = not IS_WINDOWS
SUPPORTS_SIGNAL_RELOAD = hasattr(signal, 'SIGUSR1')


def get_stdin() -> int:
    '''Returns the file descriptor for stdin.'''
    return sys.stdin.fileno()


def run_program(program_args: list[str]) -> int:
    '''Spawn a program in a PTY and return the master file descriptor.

    Raises:
        OSError: If PTY spawning is not supported on this platform.
    '''
    if not SUPPORTS_PTY:
        raise OSError(
            'interactive program wrapping requires a POSIX terminal '
            '(Linux, macOS, or WSL on Windows)')

    # Imported lazily so pipe-only use on Windows does not require Unix modules.
    from chromaterm.platform import unix

    return unix.run_program(program_args)


def close_data_fd(data_fd: Union[int, object]) -> None:
    '''Close a data file descriptor or socket.'''
    if isinstance(data_fd, int):
        os.close(data_fd)
    else:
        data_fd.close()


def wait_child() -> int:
    '''Return the exit status of the most recently spawned child process.'''
    if not SUPPORTS_PTY:
        return 0

    return os.wait()[1] >> 8


def setup_runtime_signals(reload_handler: Callable) -> None:
    '''Install signal handlers used while processing terminal I/O.'''
    if not SUPPORTS_PTY:
        return

    signal.signal(signal.SIGINT, signal.SIG_IGN)

    if SUPPORTS_SIGNAL_RELOAD:
        signal.signal(signal.SIGUSR1, reload_handler)


def reload_signal() -> Optional[int]:
    '''Return the signal used to reload configuration, if supported.'''
    if not SUPPORTS_SIGNAL_RELOAD:
        return None

    return signal.SIGUSR1
