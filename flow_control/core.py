class FlowException(Exception):
    """Exception to the normal execution flow."""

    def __init__(self, jumps: int = 1) -> None:
        super().__init__()

        self._jumps_remaining = jumps

    def raise_again(self) -> bool:
        """Whether the flow exception should be raised again."""
        self._jumps_remaining -= 1
        return self._jumps_remaining > 0
