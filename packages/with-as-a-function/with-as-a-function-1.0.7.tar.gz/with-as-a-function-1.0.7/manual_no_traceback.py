# Copyright 2019 Alexander Kozhevnikov <mentalisttraceur@gmail.com>
# SPDX-License-Identifier: 0BSD

"""Use context managers with a function instead of a statement.

Provides a minimal and portable interface for using context
managers with all the advantages of functions over syntax.

Note:
    This is the "no traceback" variant, for Python implementations that
    do not support getting the traceback object for an exception. It
    exists to allow code using the ``with_`` interface to gracefully
    degrade in the absence of full traceback support.
"""

__all__ = ('with_',)
__version__ = '1.0.7'


try:
    _BaseException = BaseException
except NameError:
    _BaseException = Exception


def with_(manager, action):
    """Execute an action within the scope of a context manager.

    Arguments:
        manager: The context manager instance to use.
        action: The callable to execute. Must accept the `as` value
            of the context manager as the only positional argument.

    Returns:
        Any: Return value of the executed action.
        None: If the manager suppresses an exception from the action.

    Raises:
        Any: If raised by calling the action and not suppressed by the
            manager, or if raised by the manager, or if the manager
            does not implement the context manager protocol correctly.

    Note:
        This "no traceback" variant always passes ``None`` for the
        ``traceback`` argument to the context manager's ``__exit__``,
        because it is meant for Python implementations that do not
        support getting the traceback object for an exception.
    """
    exit_ = type(manager).__exit__
    value = type(manager).__enter__(manager)
    try:
        result = action(value)
    except _BaseException as exception:
        if not exit_(manager, type(exception), exception, None):
            raise
        return None
    exit_(manager, None, None, None)
    return result
