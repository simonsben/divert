from __future__ import annotations

from typing import TypeVar, Generic, Any

Payload = TypeVar("Payload")


class Diversion(BaseException):
    """Diversion from the normal execution flow."""

    def __init__(self, jumps: int = 1) -> None:
        super().__init__("Flow exception wasn't caught by a flow edge!")

        self._jumps_remaining = jumps

    def raise_again(self, *_: Any) -> bool:
        """Whether the diversion should be raised again."""
        self._jumps_remaining -= 1
        return self._jumps_remaining > 0

    @classmethod
    def make_weak(cls, *args: Any, **kwargs: Any) -> Diversion:
        """Make weak variant of the diversion class.

        By dynamically forming it provides support for generic extensions of the base diversions.
        The minor performance hit is acceptable vs. having to maintain `WeakDiversion` instances for each extension.
        """

        class WeakDiversion(cls, Exception):
            """Weak variation of the diversion, so it can be caught by *normal* user exceptions."""

        return WeakDiversion(*args, **kwargs)


class PayloadDiversion(Diversion, Generic[Payload]):
    def __init__(self, payload: Payload, jumps: int = 1) -> None:
        super().__init__(jumps)
        self._payload = payload

    @property
    def payload(self) -> Payload:
        """Accessor for the return value"""
        return self._payload
