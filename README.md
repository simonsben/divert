# Divert

Divert the execution flow of your code.
This is useful for complex code with lots of method nesting and unpredictable return values.

Plus, no sub-dependencies.

## Example usage

For example, if we have an inner function (or multiple), we can immediately divert to a flow edge of our choice.

```python
from divert.flow import custom_flow_edge, divert


def inner_function(number: int) -> int:
    """Function that doubles the value or signals that the flow should change."""
    if number == 4:  # Stop condition for sake of example
        divert()  # If we want to specify the return value here we can instead use `payload_to_edge(VALUE)`

    return number * 2


@custom_flow_edge(default_return=42)
def outer_function() -> int:
    """Larger function that calls the inner function multiple times."""
    first_response = inner_function(2)
    second_response = inner_function(4)
    third_response = inner_function(8)

    return first_response + second_response + third_response
```

For further motivation for using the library, see [the documentation](examples/motivation.md).
For example usage, see [the examples](examples/).
