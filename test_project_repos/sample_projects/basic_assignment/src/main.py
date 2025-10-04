#!/usr/bin/env python3
"""
Basic assignment starter code.
Students should implement the hello_world function.
"""


def hello_world():
    """
    Return a greeting message.

    Returns:
        str: A greeting message
    """
    # TODO: Implement this function
    return "Hello, World!"


def add_numbers(a, b):
    """
    Add two numbers together.

    Args:
        a (int): First number
        b (int): Second number

    Returns:
        int: Sum of a and b
    """
    # TODO: Implement this function
    return a + b


if __name__ == "__main__":
    print(hello_world())
    print(f"2 + 3 = {add_numbers(2, 3)}")
