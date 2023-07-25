from typing import Callable

from pytest import mark

from divert.flow import custom_flow_edge
from divert.targeted import divert_to_target
from test.test_flow import DEFAULT_RETURN

EDGE_NAME = "test_edge"


@mark.parametrize("target_by_name", (True, False), ids=("name_target", "function_target"))
def test_targeted_jump(target_by_name: bool) -> None:
    """Ensure we can properly jump to targeted edges."""

    @custom_flow_edge(name=EDGE_NAME)
    def function(inner_function: Callable[[], None]) -> None:
        """Function with flow edge."""

        inner_function()

    def _inner_function() -> None:
        """Inner function requesting the jump."""
        target = EDGE_NAME if target_by_name else function
        divert_to_target(target, DEFAULT_RETURN)

    assert function(lambda: _inner_function()) == DEFAULT_RETURN
