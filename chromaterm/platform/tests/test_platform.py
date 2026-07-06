'''chromaterm.platform tests'''
import socket
import sys

import pytest

import chromaterm.platform


def test_get_stdin(monkeypatch):
    '''Return stdin's file descriptor.'''
    monkeypatch.setattr(sys.stdin, 'fileno', lambda: 0)
    assert chromaterm.platform.get_stdin() == 0


def test_posix_capabilities():
    '''POSIX platforms support PTY spawning and signal-based reload.'''
    if sys.platform == 'win32':
        pytest.skip('POSIX-only capability check')

    assert chromaterm.platform.SUPPORTS_PTY is True
    assert chromaterm.platform.SUPPORTS_SIGNAL_RELOAD is True
    assert chromaterm.platform.reload_signal() is not None


def test_windows_capabilities(monkeypatch):
    '''Native Windows disables PTY and signal reload support.'''
    monkeypatch.setattr(chromaterm.platform, 'IS_WINDOWS', True)
    monkeypatch.setattr(chromaterm.platform, 'SUPPORTS_PTY', False)
    monkeypatch.setattr(chromaterm.platform, 'SUPPORTS_SIGNAL_RELOAD', False)

    assert chromaterm.platform.reload_signal() is None
    assert chromaterm.platform.wait_child() == 0

    with pytest.raises(OSError, match='POSIX'):
        chromaterm.platform.run_program(['echo'])


def test_read_ready_windows_pipe_fallback(monkeypatch):
    '''Pipe fds on Windows use a select fallback instead of raising.'''
    import chromaterm.__main__

    monkeypatch.setattr(chromaterm.__main__.sys, 'platform', 'win32')

    assert chromaterm.__main__.read_ready(0) == [0]
    assert chromaterm.__main__.read_ready(0, timeout=0) == []


def test_read_ready_windows_socket(monkeypatch):
    '''Sockets on Windows still use select.'''
    import chromaterm.__main__

    monkeypatch.setattr(chromaterm.__main__.sys, 'platform', 'win32')

    read, write = socket.socketpair()
    write.send(b'x')

    try:
        assert read in chromaterm.__main__.read_ready(read, timeout=1)
    finally:
        read.close()
        write.close()
