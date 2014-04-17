"""
An asyncio event loop on top of the Twisted reactor.
"""

from collections import namedtuple

from asyncio.unix_events import SelectorEventLoop
from asyncio.base_events import BaseEventLoop

from twisted.internet.abstract import FileDescriptor


class _Callable(namedtuple("_Callable", "f args")):
    """
    A callable and its args, packaged in a comparable object.
    """
    def __call__(self):
        pass#return self.f(*self.args)


class _GenericFileDescriptor(FileDescriptor):
    """
    Dispatch read/write events to given callbacks.
    """
    def __init__(self, reactor, fd, readCallback, writeCallback):
        FileDescriptor.__init__(self, reactor)
        self._fd = fd
        self._readCallback = readCallback
        self._writeCallback = writeCallback

    def doRead(self):
        pass#self._readCallback()

    def doWrite(self):
        pass#self._writeCallback()

    def fileno(self):
        return self._fd


_noop = _Callable(lambda: None, ())



class TwistedEventLoop(SelectorEventLoop):
    """
    Asyncio event loop wrapping Twisted's reactor.
    """
    def __init__(self, reactor):
        BaseEventLoop.__init__(self)
        self._reactor = reactor

    def add_reader(self, fd, callback, *args):
        reader = _GenericFileDescriptor(self._reactor,
                                        fd, _Callable(callback, args), _noop)
        self._reactor.addReader(reader)

    def add_writer(self, fd, callback, *args):
        writer = _GenericFileDescriptor(self._reactor,
                                        fd, _noop, _Callable(callback, args))
        self._reactor.addWriter(writer)

    def remove_reader(self, fd):
        pass

    def remove_writer(self, fd):
        pass
