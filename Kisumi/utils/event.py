from typing import (
    Any,
    Union,
    Awaitable,
    Callable,
)
import asyncio

Subcribable = Union[
    Awaitable,
    Callable[[Any], Awaitable]
]

class Event:
    """A subscribable internal event hook allowing for subscribe and 
    publish events."""

    __slots__ = (
        "_sub_awaitables",
        "_sub_corofunc",
    )

    def __init__(self) -> None:
        """Initialises a default event."""

        self._sub_awaitables = []
        self._sub_corofunc = []
    
    def subscribe(self, hook: Subcribable) -> None:
        """Subscribes a coroutine function or an awaitable to the event."""

        if asyncio.iscoroutinefunction(hook):
            self._sub_corofunc.append(hook)
        elif asyncio.iscoroutine(hook):
            self._sub_awaitables.append(hook)
        else:
            raise TypeError(
                "Hook must be coroutine or coroutine function!"
            )
    
    async def sync_call(self, *args) -> None:
        """Sequentially calls all of the subscribed events, waiting for
        all to finish. Calls all coro funcs with `*args` as arguments.
        
        Note:
            Coroutine functions are executed first.
        """

        for coro_func in self._sub_corofunc:
            await coro_func(*args)
        
        for coro in self._sub_awaitables:
            await coro
    
    async def call(self, *args) -> Awaitable[None]:
        """Creates a new task on the current running loop and runs
        `Event.sync_call`."""

        loop = asyncio.get_running_loop()

        loop.create_task(
            self.sync_call(*args),
        )
