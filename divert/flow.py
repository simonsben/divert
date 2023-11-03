from typing import TypeVar, Callable, ParamSpec, Any

from divert.core import Diversion, PayloadDiversion

Arguments = ParamSpec("Arguments")
Return = TypeVar("Return")

Function = Callable[Arguments, Return]
OptionalFunction = Callable[Arguments, Return | None]

DefaultReturn = TypeVar("DefaultReturn")
FlowEdgeWrapper = Callable[[Function], OptionalFunction]

DiversionType = TypeVar("DiversionType", bound=Diversion)


def custom_flow_edge(default_return: DefaultReturn = None, name: str | None = None) -> FlowEdgeWrapper:
    """Flow edge that allows the default return value to be specified."""

    def flow_edge_wrapper(function: Function) -> OptionalFunction:
        """Function wrapper that defines the edge of the flow exception."""

        def wrapped_function(*args: Arguments.args, **kwargs: Arguments.kwargs) -> Return | DefaultReturn:
            """Wrapped function call for the original function, that includes the flow exception edge."""
            try:
                return function(*args, **kwargs)  # Pass through the arguments and execute function

            except Diversion as diversion:  # If a diversion occurs, catch it
                if diversion.raise_again(wrapped_function, name):  # Check if we want to jump to the next edge
                    raise

                if isinstance(diversion, PayloadDiversion):
                    return diversion.payload
                return default_return

        return wrapped_function

    return flow_edge_wrapper


def flow_edge(function: Function) -> OptionalFunction:
    """Basic execution flow edge with a null return."""
    return custom_flow_edge(default_return=None)(function)


def finalize_diversion(diversion: type[DiversionType], weak: bool) -> type[DiversionType]:
    """Finalize the diversion class."""
    return Diversion.make_weak if weak else diversion


def divert(number_of_edges: int = 1, weak: bool = False) -> None:
    """Jump to the nearest execution flow edge."""
    raise finalize_diversion(Diversion, weak)(number_of_edges)


def divert_payload(payload: Any, number_of_edges: int = 1, weak: bool = False) -> None:
    """Divert the payload to the nearest execution flow edge."""
    raise finalize_diversion(PayloadDiversion, weak)(payload, number_of_edges)
