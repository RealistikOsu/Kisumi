from typing import Type, Any, TypeVar
import threading

_singleton_reg: dict[Type[Any], Any] = {}
_singleton_lock = threading.Lock()
T = TypeVar("T")


class Singleton:
    """
    An inherited class that ensures that only one instance of the child class
    can exist at once.
    Implementation details:
        This overrides the `__new__` method.
        Running the constructor acquires an non-async, global singleton lock to
            avoid any cases in which an object can be created twice.
    """

    def __new__(cls: Type[T], *args, **kwargs) -> T:
        with _singleton_lock:
            # Main logic for ensuring only one instance of the class exists.
            if ret := _singleton_reg.get(cls):
                return ret

            # An instance has yet to be created. Create it and register it.
            ret = super().__new__(cls, *args, **kwargs)
            _singleton_reg[cls] = ret

            return ret
