from flow_control.flow import custom_flow_edge
from flow_control.targeted import to_edge_target

EDGE_NAME = "descriptive_edge_name"


def innermost_function(number: int) -> int:
    """Innermost function."""
    if number == 4:
        to_edge_target(EDGE_NAME, payload=number)  # Pass back a specific value
    return number * 3


def intermediate_function(number: int) -> int:
    """Intermediate function."""
    intermediate_number = innermost_function(number)
    return intermediate_number * 2


@custom_flow_edge(name=EDGE_NAME)
def outer_function(base: int, steps: int) -> int:
    """Outermost function."""
    value = 0
    for power in range(steps):
        result = intermediate_function(base ** power)
        print(f"{result} will be added to {value}")

        value += result

    return value


if __name__ == "__main__":
    print("Clean execution result:", outer_function(3, 3))
    print("Stopped execution result:", outer_function(2, 4))
