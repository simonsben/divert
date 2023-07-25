def nested_function(number: int, should_stop: bool = False) -> int | None:
    """Example of a nested function that doubles values."""
    if should_stop:
        return None

    return number * 2


def my_function() -> int | None:
    """Example function that makes multiple calls."""
    # Example nested calls that succeed
    if (first_return := nested_function(2)) is None:
        return None
    print("First call:", first_return)

    if (second_return := nested_function(4)) is None:
        return None
    print("Second call:", second_return)

    if (third_return := nested_function(8)) is None:
        return None
    print("Third call:", third_return)

    if (fourth_return := nested_function(16, should_stop=True)) is None:  # Nested function wants to stop the execution
        return None
    print("Shouldn't print!:", fourth_return)

    if (fifth_return := nested_function(32)) is None:
        return None
    print("I shouldn't have run!", fifth_return)

    return 42


if __name__ == "__main__":
    print("Executing basic example.")
    function_return = my_function()
    print("Completed execution, return:", function_return)
