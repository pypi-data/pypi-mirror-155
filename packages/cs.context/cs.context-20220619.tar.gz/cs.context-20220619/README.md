Assorted context managers.

*Latest release 20220619*:
twostep: the returned "tear down" phase function needs to ignore StopIteration from the context manager, see PEP 479.

## Class `ContextManagerMixin`

A mixin to provide context manager `__enter__` and `__exit__` methods
running the first and second steps of a single `__enter_exit__` generator method.

*Note*: the `__enter_exit__` method is _not_ a context manager,
but a short generator method.

This makes it easy to use context managers inside `__enter_exit__`
as the setup/teardown process, for example:

    def __enter_exit__(self):
        with open(self.datafile, 'r') as f:
            yield f

Like a context manager created via `@contextmanager`
it performs the setup phase and then `yield`s the value for the `with` statement.
If `None` is `yield`ed (as from a bare `yield`)
then `self` is returned from `__enter__`.
As with `@contextmanager`,
if there was an exception in the managed suite
then that exception is raised on return from the `yield`.

*However*, and _unlike_ an `@contextmanager` method,
the `__enter_exit__` generator _may_ also `yield`
an additional true/false value to use as the result
of the `__exit__` method, to indicate whether the exception was handled.
This extra `yield` is _optional_ and if it is omitted the `__exit__` result
will be `False` indicating that an exception was not handled.

Here is a sketch of a method which can handle a `SomeException` specially:

    class CMgr(ContextManagerMixin):
        def __enter_exit__(self):
            ... do some setup here ...
            # Returning self is common, but might be any relevant value.
            # Note that if you want `self`, you can just use a bare yield
            # and ContextManagerMixin will provide `self` as the default.
            enter_result = self
            exit_result = False
            try:
                yield enter_result
            except SomeException as e:
                ... handle e ...
                exit_result = True
            finally:
                ... do tear down here ...
            yield exit_result

*Method `ContextManagerMixin.__enter__(self)`*:
Run `super().__enter__` (if any)
then the `__enter__` phase of `self.__enter_exit__()`.

*Method `ContextManagerMixin.__exit__(self, exc_type, exc_value, traceback)`*:
Run the `__exit__` step of `self.__enter_exit__()`,
then `super().__exit__` (if any).

## Function `pop_cmgr(o, attr)`

Run the `__exit__` phase of a context manager commenced with `push_cmgr`.
Restore `attr` as it was before `push_cmgr`.
Return the result of `__exit__`.

## Function `popattrs(o, attr_names, old_values)`

The "pop" part of `stackattrs`.
Restore previous attributes of `o`
named by `attr_names` with previous state in `old_values`.

This can be useful in hooks/signals/callbacks,
where you cannot inline a context manager.

## Function `popkeys(d, key_names, old_values)`

The "pop" part of `stackkeys`.
Restore previous key values of `d`
named by `key_names` with previous state in `old_values`.

This can be useful in hooks/signals/callbacks,
where you cannot inline a context manager.

## Function `push_cmgr(o, attr, cmgr)`

A convenience wrapper for `twostep(cmgr)`
to run the `__enter__` phase of `cmgr` and save its value as `o.`*attr*`.
Return the result of the `__enter__` phase.

The `__exit__` phase is run by `pop_cmgr(o,attr)`,
returning the return value of the exit phase.

Example use in a unit test:

    class TestThing(unittest.TestCase):
        def setUp(self):
            # save the temp dir path as self.dirpath
            push_cmgr(self, 'dirpath', TemporaryDirectory())
        def tearDown(self):
            # clean up the temporary directory, discard self.dirpath
            pop_cmgr(self, 'dirpath')

The `cs.testutils` `SetupTeardownMixin` class does this
allowing the provision of a single `setupTeardown()` context manager method
for test case setUp/tearDown.

Doc test:

    >>> from os.path import isdir as isdirpath
    >>> from tempfile import TemporaryDirectory
    >>> from types import SimpleNamespace
    >>> obj = SimpleNamespace()
    >>> dirpath = push_cmgr(obj, 'path', TemporaryDirectory())
    >>> assert dirpath == obj.path
    >>> assert isdirpath(dirpath)
    >>> pop_cmgr(obj, 'path')
    >>> assert not hasattr(obj, 'path')
    >>> assert not isdirpath(dirpath)

## Function `pushattrs(o, **attr_values)`

The "push" part of `stackattrs`.
Push `attr_values` onto `o` as attributes,
return the previous attribute values in a dict.

This can be useful in hooks/signals/callbacks,
where you cannot inline a context manager.

## Function `pushkeys(d, **key_values)`

The "push" part of `stackkeys`.
Push `key_values` onto `d` as key values.
return the previous key values in a dict.

This can be useful in hooks/signals/callbacks,
where you cannot inline a context manager.

## Function `setup_cmgr(cmgr)`

Run the set up phase of the context manager `cmgr`
and return a callable which runs the tear down phase.

This is a convenience wrapper for the lower level `twostep()` function
which produces a two iteration generator from a context manager.

Please see the `push_cmgr` function, a superior wrapper for `twostep()`.

*Note*:
this function expects `cmgr` to be an existing context manager.
In particular, if you define some context manager function like this:

    @contextmanager
    def my_cmgr_func(...):
        ...
        yield
        ...

then the correct use of `setup_cmgr()` is:

    teardown = setup_cmgr(my_cmgr_func(...))

and _not_:

    cmgr_iter = setup_cmgr(my_cmgr_func)
    ...

The purpose of `setup_cmgr()` is to split any context manager's operation
across two steps when the set up and teardown phases must operate
in different parts of your code.
A common situation is the `__enter__` and `__exit__` methods
of another context manager class.

The call to `setup_cmgr()` performs the "enter" phase
and returns the tear down callable.
Calling that performs the tear down phase.

Example use in a class:

    class SomeClass:
        def __init__(self, foo)
            self.foo = foo
            self._teardown = None
        def __enter__(self):
            self._teardown = setup_cmgr(stackattrs(o, setting=foo))
        def __exit__(self, *_):
            teardown, self._teardown = self._teardown, None
            teardown()

## Class `StackableState(_thread._local)`

An object which can be called as a context manager
to push changes to its attributes.

Example:

    >>> state = StackableState(a=1, b=2)
    >>> state.a
    1
    >>> state.b
    2
    >>> state
    StackableState(a=1,b=2)
    >>> with state(a=3, x=4):
    ...     print(state)
    ...     print("a", state.a)
    ...     print("b", state.b)
    ...     print("x", state.x)
    ...
    StackableState(a=3,b=2,x=4)
    a 3
    b 2
    x 4
    >>> state.a
    1
    >>> state
    StackableState(a=1,b=2)

*Method `StackableState.__call__(self, **kw)`*:
Calling an instance is a context manager yielding `self`
with attributes modified by `kw`.

## Function `stackattrs(o, **attr_values)`

Context manager to push new values for the attributes of `o`
and to restore them afterward.
Returns a `dict` containing a mapping of the previous attribute values.
Attributes not present are not present in the mapping.

Restoration includes deleting attributes which were not present
initially.

This makes it easy to adjust temporarily some shared context object
without having to pass it through the call stack.

See `stackkeys` for a flavour of this for mappings.

Example of fiddling a programme's "verbose" mode:

    >>> class RunModes:
    ...     def __init__(self, verbose=False):
    ...         self.verbose = verbose
    ...
    >>> runmode = RunModes()
    >>> if runmode.verbose:
    ...     print("suppressed message")
    ...
    >>> with stackattrs(runmode, verbose=True):
    ...     if runmode.verbose:
    ...         print("revealed message")
    ...
    revealed message
    >>> if runmode.verbose:
    ...     print("another suppressed message")
    ...

Example exhibiting restoration of absent attributes:

    >>> class O:
    ...     def __init__(self):
    ...         self.a = 1
    ...
    >>> o = O()
    >>> print(o.a)
    1
    >>> print(o.b)
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    AttributeError: 'O' object has no attribute 'b'
    >>> with stackattrs(o, a=3, b=4):
    ...     print(o.a)
    ...     print(o.b)
    ...     o.b = 5
    ...     print(o.b)
    ...     delattr(o, 'a')
    ...
    3
    4
    5
    >>> print(o.a)
    1
    >>> print(o.b)
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    AttributeError: 'O' object has no attribute 'b'

## Function `stackkeys(d, **key_values)`

Context manager to push new values for the key values of `d`
and to restore them afterward.
Returns a `dict` containing a mapping of the previous key values.
Keys not present are not present in the mapping.

Restoration includes deleting key values which were not present
initially.

This makes it easy to adjust temporarily some shared context object
without having to pass it through the call stack.

See `stackattrs` for a flavour of this for object attributes.

Example of making log entries which may reference
some higher level context log entry:

    >>> import time
    >>> global_context = {
    ...     'parent': None,
    ... }
    >>> def log_entry(desc, **kw):
    ...     print("log_entry: global_context =", repr(global_context))
    ...     entry = dict(global_context)
    ...     entry.update(desc=desc, when=time.time())
    ...     entry.update(kw)
    ...     return entry
    ...
    >>> log_entry("stand alone entry")    #doctest: +ELLIPSIS
    log_entry: global_context = {'parent': None}
    {'parent': None, 'desc': 'stand alone entry', 'when': ...}
    >>> context_entry = log_entry("high level entry")
    log_entry: global_context = {'parent': None}
    >>> context_entry                     #doctest: +ELLIPSIS
    {'parent': None, 'desc': 'high level entry', 'when': ...}
    >>> with stackkeys(global_context, parent=context_entry): #doctest: +ELLIPSIS
    ...     print(repr(log_entry("low level event")))
    ...
    log_entry: global_context = {'parent': {'parent': None, 'desc': 'high level entry', 'when': ...}}
    {'parent': {'parent': None, 'desc': 'high level entry', 'when': ...}, 'desc': 'low level event', 'when': ...}
    >>> log_entry("another standalone entry")    #doctest: +ELLIPSIS
    log_entry: global_context = {'parent': None}
    {'parent': None, 'desc': 'another standalone entry', 'when': ...}

## Function `twostep(cmgr)`

Return a generator which operates the context manager `cmgr`.

The first iteration performs the "enter" phase and yields the result.
The second iteration performs the "exit" phase and yields `None`.

See also the `push_cmgr(obj,attr,cmgr)` function
and its partner `pop_cmgr(obj,attr)`
which form a convenience wrapper for this low level generator.

The purpose of `twostep()` is to split any context manager's operation
across two steps when the set up and tear down phases must operate
in different parts of your code.
A common situation is the `__enter__` and `__exit__` methods
of another context manager class
or the `setUp` and `tearDown` methods of a unit test case.

*Note*:
this function expects `cmgr` to be an existing context manager
and _not_ the function which returns the context manager.

In particular, if you define some function like this:

    @contextmanager
    def my_cmgr_func(...):
        ...
        yield
        ...

then the correct use of `twostep()` is:

    cmgr_iter = twostep(my_cmgr_func(...))
    next(cmgr_iter)   # set up
    next(cmgr_iter)   # tear down

and _not_:

    cmgr_iter = twostep(my_cmgr_func)
    next(cmgr_iter)   # set up
    next(cmgr_iter)   # tear down

Example use in a class (but really, use `push_cmgr`/`pop_cmgr` instead):

    class SomeClass:
        def __init__(self, foo)
            self.foo = foo
            self._cmgr_ = None
        def __enter__(self):
            self._cmgr_stepped = twostep(stackattrs(o, setting=foo))
            self._cmgr = next(self._cmgr_stepped)
            return self._cmgr
        def __exit__(self, *_):
            next(self._cmgr_stepped)
            self._cmgr = None

# Release Log



*Release 20220619*:
twostep: the returned "tear down" phase function needs to ignore StopIteration from the context manager, see PEP 479.

*Release 20220227*:
New stack_signals context manager to push signal handlers.

*Release 20211115.1*:
Docstring grammar/phrasing updates.

*Release 20211115*:
Rename `enter_exit` to `__enter_exit__` - the user doesn't call this overtly and it aligns better with `__enter__` and `__exit__`.

*Release 20211114.1*:
ContextManagerMixin: the default __enter__ return is self, supporting a trivial bare `yield` in the generator.

*Release 20211114*:
New ContextManagerMixin mixin class to implement the __enter__/__exit__ methods using a simple generator function named enter_exit.

*Release 20210727*:
* twostep: iteration 1 now returns the result of __enter__, iteration 2 now returns None.
* New functions push_cmgr(obj,attr,cmgr) and partner pop_cmgr(obj,attr) to run a twostep()ed context manager conveniently, more conveniently than setup_cmgr().

*Release 20210420.1*:
Rerelease after completing stalled merge: docstring updates.

*Release 20210420*:
Docstring corrections and improvements.

*Release 20210306*:
* New twostep() and setup_cmgr() functions to split a context manager into set up and teardown phases for when these must occur in different parts of the code.
* New thread local StackableState class which can be called to push attribute changes with stackattrs - intended for use as shared global state to avoiod passing through deep function call chains.

*Release 20200725.1*:
Docstring improvements.

*Release 20200725*:
New stackkeys and components pushkeys and popkeys doing "stackattrs for dicts/mappings".

*Release 20200517*:
* Add `nullcontext` like the one from recent contextlib.
* stackattrs: expose the push and pop parts as pushattrs() and popattrs().

*Release 20200228.1*:
Initial release with stackattrs context manager.
