import multiprocessing
import asyncio
import inspect

from .separate_thread import KlassThreadWrapper
from .separate_process import KlassProcessWrapper

DEFAULT_METHODS = ["start", "stop"]


ISOLATION_TYPES = {"thread": KlassThreadWrapper, "process": KlassProcessWrapper}


def run_separately_as(isolation_type):
    """
    Only ISOLATION_TYPES supported.
    If you put in "thread", we take your class, wrap it up and let it run in
    its own thread, and you can write a top level #run function that we call
    when your thread has been instantiated. The advantage of using this over
    Thread explicitly is that you can use an asynchronous #run method and we
    will pass you the event loop.

    If you put in "process", we will take your class, wrap it up inside a
    separate process, and you just need to denote a top level #run function.
    If your object is pickleable, we will endevour to return it back to you
    once #stop has been called on it. If it isn't, then you'll have to take
    our word for it that it has operated correctly. If there has been an
    error during operation, we will endevour to bring the error back and
    raise it as if it were your class whose operation has malfunctioned,
    and hide the process abstraction away from you.
    """
    try:
        klass_wrapper = ISOLATION_TYPES[isolation_type]
    except KeyError:
        raise NotSupportedError(
            f"{isolation_type} not supported, chose from {ISOLATION_TYPES}"
        )

    def wrap_klass(user_defined_klass):
        wrapper = klass_wrapper(user_defined_klass)
        wrapper.__name__ = user_defined_klass.__name__
        return wrapper

    return wrap_klass
