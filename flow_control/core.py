from typing import Any, TypeVar, Generic


class FlowException(Exception):
    """Exception to the normal execution flow."""

    def __init__(self, jumps: int = 1) -> None:
        super().__init__()

        self._jumps_remaining = jumps

    def raise_again(self) -> bool:
        """Whether the flow exception should be raised again."""
        self._jumps_remaining -= 1
        return self._jumps_remaining > 0


Payload = TypeVar("Payload")


class PayloadFlowException(FlowException, Generic[Payload]):
    def __init__(self, payload: Payload, jumps: int = 1) -> None:
        super().__init__(jumps)
        self._payload = payload

    @property
    def payload(self) -> Payload:
        """Accessor for the return value"""
        return self._payload
