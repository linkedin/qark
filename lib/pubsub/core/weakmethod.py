"""
This module provides a basic "weak method" implementation, WeakMethod. It uses
weakref.WeakRef which, used on its own, produces weak methods that are dead on
creation, not very useful. Use the getWeakRef(object) module function to create the
proper type of weak reference (weakref.WeakRef or WeakMethod) for given object.

:copyright: Copyright since 2006 by Oliver Schoenborn, all rights reserved.
:license: BSD, see LICENSE_BSD_Simple.txt for details.

"""

# for function and method parameter counting:
from inspect import ismethod
# for weakly bound methods:
from types import MethodType
from weakref import ref as WeakRef


class WeakMethod:
    """Represent a weak bound method, i.e. a method which doesn't keep alive the
    object that it is bound to. """

    def __init__(self, method, notifyDead = None):
        """The method must be bound. notifyDead will be called when
        object that method is bound to dies. """
        assert ismethod(method)
        if method.__self__ is None:
            raise ValueError('Unbound methods cannot be weak-referenced.')

        self.notifyDead = None
        if notifyDead is None:
            self.objRef = WeakRef(method.__self__)
        else:
            self.notifyDead = notifyDead
            self.objRef = WeakRef(method.__self__, self.__onNotifyDeadObj)

        self.fun = method.__func__
        self.cls = method.__self__.__class__

    def __onNotifyDeadObj(self, ref):
        if self.notifyDead:
            try:
                self.notifyDead(self)
            except Exception:
                import traceback
                traceback.print_exc()

    def __call__(self):
        """Returns a MethodType if object for method still alive.
        Otherwise return None. Note that MethodType causes a
        strong reference to object to be created, so shouldn't save
        the return value of this call. Note also that this __call__
        is required only for compatibility with WeakRef.ref(), otherwise
        there would be more efficient ways of providing this functionality."""
        if self.objRef() is None:
            return None
        else:
            return MethodType(self.fun, self.objRef())

    def __eq__(self, method2):
        """Two WeakMethod objects compare equal if they refer to the same method
        of the same instance. Thanks to Josiah Carlson for patch and clarifications
        on how dict uses eq/cmp and hashing. """
        if not isinstance(method2, WeakMethod):
            return False

        return (    self.fun      is method2.fun
                and self.objRef() is method2.objRef()
                and self.objRef() is not None )

    def __hash__(self):
        """Hash is an optimization for dict searches, it need not
        return different numbers for every different object. Some objects
        are not hashable (eg objects of classes derived from dict) so no
        hash(objRef()) in there, and hash(self.cls) would only be useful
        in the rare case where instance method was rebound. """
        return hash(self.fun)

    def __repr__(self):
        dead = ''
        if self.objRef() is None:
            dead = '; DEAD'
        obj = '<%s at %s%s>' % (self.__class__, id(self), dead)
        return obj

    def refs(self, weakRef):
        """Return true if we are storing same object referred to by weakRef."""
        return self.objRef == weakRef


def getWeakRef(obj, notifyDead=None):
    """Get a weak reference to obj. If obj is a bound method, a WeakMethod
    object, that behaves like a WeakRef, is returned; if it is
    anything else a WeakRef is returned. If obj is an unbound method,
    a ValueError will be raised."""
    if ismethod(obj):
        createRef = WeakMethod
    else:
        createRef = WeakRef

    return createRef(obj, notifyDead)

