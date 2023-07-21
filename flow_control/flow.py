from typing import TypeVar, Callable, ParamSpec, Any

from flow_control.core import FlowException, PayloadFlowException

Arguments = ParamSpec("Arguments")
Return = TypeVar("Return")

Function = Callable[Arguments, Return]
OptionalFunction = Callable[Arguments, Return | None]

DefaultReturn = TypeVar("DefaultReturn")


def custom_flow_edge(default_return: DefaultReturn) -> Callable[[Function], OptionalFunction]:
    """Flow edge that allows the default return value to be specified."""

    def flow_edge_wrapper(function: Function) -> OptionalFunction:
        """Function wrapper that defines the edge of the flow exception."""

        def wrapped_function(*args: Arguments.args, **kwargs: Arguments.kwargs) -> Return | DefaultReturn:
            """Wrapped function call for the original function, that includes the flow exception edge."""
            try:
                return function(*args, **kwargs)  # Pass through the arguments and execute function

            except FlowException as flow_exception:  # If a flow exception occurs, catch it
                if flow_exception.raise_again():  # Check if we want to jump to the next edge
                    raise

                if isinstance(flow_exception, PayloadFlowException):
                    return flow_exception.payload
                return default_return

        return wrapped_function

    return flow_edge_wrapper


def flow_edge(function: Function) -> OptionalFunction:
    """Basic flow edge with a null return."""
    return custom_flow_edge(default_return=None)(function)


def to_edge(number_of_edges: int = 1) -> None:
    """Jump to the nearest flow edge."""
    raise FlowException(number_of_edges)


def payload_to_edge(payload: Any, number_of_edges: int = 1) -> None:
    """Jump the payload to the nearest flow edge."""
    raise PayloadFlowException(payload, number_of_edges)
