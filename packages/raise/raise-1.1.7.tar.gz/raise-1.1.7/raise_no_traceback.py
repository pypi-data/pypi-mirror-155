# SPDX-License-Identifier: 0BSD
# Copyright 2018 Alexander Kozhevnikov <mentalisttraceur@gmail.com>

"""Raise exceptions with a function instead of a statement.

Provides a minimal, clean and portable interface for raising exceptions
with all the advantages of functions over syntax.

Note:
    This is the "no traceback" variant, for Python implementations that
    do not support using a custom traceback when raising. It exists to
    allow code using the ``raise_`` interface to gracefully degrade in
    the absence of full traceback support.
"""

__all__ = ('raise_',)
__version__ = '1.1.6'


def raise_(exception, traceback=None):
    """Raise an exception, optionally with a custom traceback.

    Arguments:
        exception: The exception instance or type to raise.
        traceback (optional): Traceback to raise the exception with.

    Note:
        This "no traceback" variant silently ignores the ``traceback``
        argument, because it is meant for Python implementations
        that do not support using a custom traceback when raising.
    """
    raise exception
