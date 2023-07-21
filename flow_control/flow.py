from typing import TypeVar, Callable, ParamSpec, Any

from flow_control.core import FlowException, PayloadFlowException

Arguments = ParamSpec("Arguments")
Return = TypeVar("Return")

Function = Callable[Arguments, Return]
OptionalFunction = Callable[Arguments, Return | None]


def flow_edge(function: Function) -> OptionalFunction:
    """Function wrapper that defines the edge of the flow exception."""

    def wrapped_function(*args: Arguments.args, **kwargs: Arguments.kwargs) -> Return | None:
        """Wrapped function call for the original function, that includes the flow exception edge."""
        try:
            return function(*args, **kwargs)  # Pass through the arguments and execute function

        except FlowException as flow_exception:  # If a flow exception occurs, catch it
            if flow_exception.raise_again():  # Check if we want to jump to the next edge
                raise

            if isinstance(flow_exception, PayloadFlowException):
                return flow_exception.payload

    return wrapped_function


def to_edge(number_of_edges: int = 1) -> None:
    """Jump to the nearest flow edge."""
    raise FlowException(number_of_edges)


def payload_to_edge(payload: Any, number_of_edges: int = 1) -> None:
    """Jump the payload to the nearest flow edge."""
    raise PayloadFlowException(payload, number_of_edges)
