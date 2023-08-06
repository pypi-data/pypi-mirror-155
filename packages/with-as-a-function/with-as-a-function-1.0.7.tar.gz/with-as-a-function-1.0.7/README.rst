Python ``with`` as a Function
=============================

Use context managers with a function instead of a statement.

Provides a minimal and portable interface for using context
managers with all the advantages of functions over syntax.

Allows using context managers on Python implementations that
are too old or too incomplete to have the ``with`` statement.


Versioning
----------

This library's version numbers follow the `SemVer 2.0.0
specification <https://semver.org/spec/v2.0.0.html>`_.


Installation
------------

::

    pip install with-as-a-function

If you need to get it manually, or you need the "no traceback"
variant, see the `Manual Installation`_ section for tips.


Usage
-----

Import ``with_``:

.. code:: python

    from with_ import with_

With it we can do things like this:

.. code:: python

    data = with_(open('my_file.txt'), lambda my_file: my_file.read())

Which is similar to:

.. code:: python

    with open('my_file.txt') as my_file:
        data = my_file.read()

And of course because ``with_`` is a function, you can combine
it with ``functools.partial`` and other functional programming
libraries and techniques for many more uses.


Portability
-----------

Portable to all releases of both Python 3 and Python 2.

*Even those without the* ``with`` *statement.*

(The oldest tested is 2.5, but it will likely work on all
Python 2 versions and probably on even earlier versions.)

For Python implementations that neither support the
``with`` statement nor have ``sys.exc_info``, a
"no traceback" variant can be installed manually.


Manual Installation
-------------------

Depending on your needs, either:

* Take one of these files and save it as ``with_.py``:

  * ``normal.py`` for Python implementations that already have
    the ``with`` statement.
  * ``from_future_import.py`` for Python implementations that
    need the line ``from __future__ import with_statement``
    to get the ``with`` statement.
  * ``manual.py`` for Python implementations that don't have
    the ``with`` statement.
  * ``manual_no_traceback.py`` for Python implementations that
    have neither the ``with`` statement nor ``sys.exc_info``.

* Take the above files that you need, and save them in a folder
  called ``with_`` along with a custom ``__init__.py`` that
  conditionally imports from the right file as needed.

That way you can always do ``from with_ import with_``
in all of your other code and it'll just work.
