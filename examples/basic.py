from divert.flow import divert, flow_edge


def nested_function(number: int, should_raise: bool = False) -> int:
    """Example of a nested function that doubles values."""
    if should_raise:
        divert()

    return number * 2


@flow_edge
def my_function() -> int:
    """Example function that makes multiple calls."""
    # Example nested calls that succeed
    print("First call:", nested_function(2))
    print("Second call:", nested_function(4))
    print("Third call:", nested_function(8))

    print("Shouldn't print!:", nested_function(16, should_raise=True))  # Nested function wants to stop the execution
    print("I shouldn't have run!", nested_function(32))

    return 42


if __name__ == "__main__":
    print("Executing basic example.")
    function_return = my_function()
    print("Completed execution, return:", function_return)
