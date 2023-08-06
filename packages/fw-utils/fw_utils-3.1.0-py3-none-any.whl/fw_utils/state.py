"""Cached application state management."""
import os
import threading
import typing as t

__all__ = ["Cached"]

T = t.TypeVar("T")


class Cached(t.Generic[T]):
    """Descriptor for caching attributes and injecting dependencies."""

    def __init__(  # pylint: disable=too-many-arguments
        self,
        init: t.Callable[..., T],
        args: t.List = None,
        clear: t.Callable[[T], None] = None,
        fork_safe: bool = False,
        thread_safe: bool = True,
    ) -> None:
        """Initialize the cached attribute descriptor.

        Args:
            init (callable): The function to init the attribute with on access.
            args (list[Cached]): List of cached attributes to load and pass to
                the init function as arguments for dependency injection.
            clear (callable): Optional callback to tear down the attribute with.
            fork_safe: (bool): Set to True to enable sharing between processes.
            thread_safe: (bool): Set to False disable sharing between threads.
        """
        self.init = init
        self.args = args or []
        self.clear = clear
        if fork_safe and not thread_safe:
            raise ValueError(  # pragma: no cover
                "Thread IDs are only unique within a single process. Using "
                "fork_safe=True and thread_safe=False is not allowed."
            )
        self.fork_safe = fork_safe
        self.thread_safe = thread_safe
        self.name = ""

    def __set_name__(self, owner: type, name: str) -> None:
        """Store the descriptor attribute name as defined on the owner class."""
        self.name = name

    def __get__(self, instance, owner: t.Optional[type] = None) -> T:
        """Return the initialized attribute (cached)."""
        # accessed as a class attribute - return the descriptor
        if instance is None:
            return self  # type: ignore
        # accessed as an instance attribute - return the attribute
        cache = self.get_cache_dict(instance)
        key = self.get_cache_key()
        # initialize the attribute if it's not cached yet
        if key not in cache:
            # dependency injection - pass other cached attrs as args
            args = [arg.__get__(instance, owner) for arg in self.args]
            cache[key] = self.init(*args)
        return cache[key]

    def __set__(self, instance, value) -> None:
        """Set arbitrary attribute value."""
        cache = self.get_cache_dict(instance)
        key = self.get_cache_key()
        cache[key] = value

    def __delete__(self, instance) -> None:
        """Delete the cached attribute."""
        cache = self.get_cache_dict(instance)
        key = self.get_cache_key()
        # tear down the attribute if it's cached
        if key in cache:
            if self.clear:
                self.clear(cache[key])
            # remove from the cache dict and call an explicit del on the attr
            del cache[key]
            del key

    @staticmethod
    def get_cache_dict(instance) -> dict:
        """Return the cache dict of the given instance."""
        return instance.__dict__.setdefault("_cached", {})

    def get_cache_key(self) -> str:
        """Return the cache key based on multiprocess/thread safety."""
        key = f"/{self.name}"
        if not self.fork_safe:
            key = f"{key}/pid:{os.getpid()}"
        if not self.thread_safe:
            key = f"{key}/tid:{threading.get_ident()}"
        return key
