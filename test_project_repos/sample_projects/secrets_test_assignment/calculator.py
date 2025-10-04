"""
Calculator Assignment - Main Implementation File

This is a sample calculator assignment for testing secrets management functionality.
Students implement basic calculator operations while instructor tests use secrets
to access private test repositories.
"""


def add(a: float, b: float) -> float:
    """Add two numbers."""
    return a + b


def subtract(a: float, b: float) -> float:
    """Subtract second number from first."""
    return a - b


def multiply(a: float, b: float) -> float:
    """Multiply two numbers."""
    return a * b


def divide(a: float, b: float) -> float:
    """Divide first number by second."""
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b


def main():
    """Main function for manual testing."""
    print("Calculator Assignment")
    print("===================")

    # Test cases
    print(f"add(5, 3) = {add(5, 3)}")
    print(f"subtract(10, 4) = {subtract(10, 4)}")
    print(f"multiply(6, 7) = {multiply(6, 7)}")
    print(f"divide(15, 3) = {divide(15, 3)}")


if __name__ == "__main__":
    main()
