from typing import Any

from pytest import mark
from unittest.mock import MagicMock

from flow_control.core import PayloadFlowException, FlowException
from flow_control.flow import custom_flow_edge

DEFAULT_RETURN = 42


def get_return(exception: FlowException) -> Any:
    """Wrap and mock a function with a flow edge and the inner function, then get the return from the edge wrapper."""
    inner_function = MagicMock(side_effect=exception)

    @custom_flow_edge(default_return=DEFAULT_RETURN)
    def function() -> int:
        inner_function()

        return 0

    return function()


def test_default_return() -> None:
    """Ensure the wrapper properly returns the default value."""
    assert get_return(FlowException()) == DEFAULT_RETURN, "Didn't return the default value."


@mark.parametrize("payload", (None, DEFAULT_RETURN, DEFAULT_RETURN * 2, {"some": "thing"}))
def test_custom_flow_edge(payload: Any) -> None:
    """Ensure that the custom flow edge works properly."""
    assert get_return(PayloadFlowException(payload)) == payload, "Return value was different than expected."
