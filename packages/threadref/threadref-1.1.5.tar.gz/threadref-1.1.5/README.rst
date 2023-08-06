``weakref`` for Threads
=======================

Allows threads in Python to create "weak references"
to themselves that detect when the thread is no longer
running, similar to how a weak reference detects when
its referent object is no longer alive.

Provides a lightweight way for one or more independent
pieces of code to register per-thread cleanup callbacks
without coordination.


Versioning
----------

This library's version numbers follow the `SemVer 2.0.0
specification <https://semver.org/spec/v2.0.0.html>`_.


Installation
------------

::

    pip install threadref


Usage
-----

.. code:: python

    import threadref

Create a reference to the current thread, with a
callback that will fire when the thread exits:

.. code:: python

    reference = threadref.ref(lambda reference: ...)

Just like ``weakref.ref``, ``threadref.ref`` instances
must still be alive when their referent thread stops
running, or their callback will not be called.

Create a finalizer for the current thread, which
will be called when the thread exits:

.. code:: python

    finalizer = threadref.finalize(function, *args, **kwargs)

Just like ``weakref.finalize``, ``threadref.finalize``
instances remain alive on their own as long as they
need to, so this is a simpler and nicer interface in
the typical case of registering cleanup functions.

Details
~~~~~~~

``threadref.ref`` and ``threadref.finalize`` wrap
``weakref.ref`` and ``weakref.finalize``, and the
interface is the same except that they act as if
they are referencing the thread itself instead of
taking a referent argument, and internally they
work by referencing an object saved on a private
``threading.local`` instance.
