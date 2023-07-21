from typing import Callable

from flow_control.flow import flow_edge
from flow_control.targeted import to_edge_target
from test.test_flow import DEFAULT_RETURN


def test_targeted_jump() -> None:
    @flow_edge
    def function(inner_function: Callable[[], None]) -> None:
        """Function with flow edge."""

        inner_function()

    def _inner_function() -> None:
        """Inner function requesting the jump."""
        to_edge_target(function, DEFAULT_RETURN)

    assert function(lambda: _inner_function()) == DEFAULT_RETURN
