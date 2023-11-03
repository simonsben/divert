from typing import Callable, TypeVar

from divert.core import PayloadDiversion, Payload
from divert.flow import finalize_diversion

Target = TypeVar("Target", bound=Callable | str | None)


class TargetedDiversion(PayloadDiversion):
    def __init__(self, target: Target, payload: Payload) -> None:
        super().__init__(payload)
        self._target = target

    def raise_again(self, edge_function: Callable, name: str | None) -> bool:
        """Whether the current edge is the stopping point."""
        if self._target is None:
            return True

        target_subject = edge_function if callable(self._target) else name
        return self._target != target_subject


def divert_to_target(target: Target, payload: Payload = None, weak: bool = False) -> None:
    """Divert the payload to a flow edge specified by the function it wraps or the edge name."""
    raise finalize_diversion(TargetedDiversion, weak)(target, payload)
