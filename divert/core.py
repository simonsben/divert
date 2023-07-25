from typing import TypeVar, Generic, Any

Payload = TypeVar("Payload")


class Diversion(Exception):
    """Diversion from the normal execution flow."""

    def __init__(self, jumps: int = 1) -> None:
        super().__init__("Flow exception wasn't caught by a flow edge!")

        self._jumps_remaining = jumps

    def raise_again(self, *_: Any) -> bool:
        """Whether the diversion should be raised again."""
        self._jumps_remaining -= 1
        return self._jumps_remaining > 0


class PayloadDiversion(Diversion, Generic[Payload]):
    def __init__(self, payload: Payload, jumps: int = 1) -> None:
        super().__init__(jumps)
        self._payload = payload

    @property
    def payload(self) -> Payload:
        """Accessor for the return value"""
        return self._payload
