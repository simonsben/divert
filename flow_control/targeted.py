from typing import Callable

from flow_control.core import PayloadFlowException, Payload


class TargetedFlowException(PayloadFlowException):
    def __init__(self, target: Callable, payload: Payload) -> None:
        super().__init__(payload)
        self._target = target

    def raise_again(self, edge_function: Callable) -> bool:
        """Whether the current edge function is the stopping point."""
        return edge_function != self._target


def to_edge_target(target: Callable, payload: Payload = None) -> None:
    """Jump the payload to an edge specified by the function it wraps."""
    raise TargetedFlowException(target, payload)
