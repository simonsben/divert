from pytest import mark

from divert.core import Diversion


@mark.parametrize("jumps", argvalues=range(10))
def test_flow_exception__raise_again(jumps: int) -> None:
    """Ensure that the exception properly tracks how many levels it has jumped."""
    flow_exception = Diversion(jumps=jumps)
    for index in range(jumps):
        current_jump = index + 1
        if flow_exception.raise_again():
            assert current_jump < jumps, f"Should have stopped execution before {current_jump}"

        else:
            assert current_jump >= jumps, f"Should have continued jumping at {current_jump}"
