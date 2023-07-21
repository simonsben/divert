from typing import Callable, TypeVar

from flow_control.core import PayloadFlowException, Payload

Target = TypeVar("Target", bound=Callable | str | None)


class TargetedFlowException(PayloadFlowException):
    def __init__(self, target: Target, payload: Payload) -> None:
        super().__init__(payload)
        self._target = target

    def raise_again(self, edge_function: Callable, name: str | None) -> bool:
        """Whether the current edge function is the stopping point."""
        if self._target is None:
            return True

        target_subject = edge_function if callable(self._target) else name
        return self._target != target_subject


def to_edge_target(target: Target, payload: Payload = None) -> None:
    """Jump the payload to an edge specified by the function it wraps or the edge name."""
    raise TargetedFlowException(target, payload)
