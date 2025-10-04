"""
Solution file for Calculator Assignment

This file contains complete solutions for instructor reference and testing.
"""


def add(a: float, b: float) -> float:
    """Add two numbers with comprehensive validation."""
    if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
        raise TypeError("Arguments must be numbers")
    return a + b


def subtract(a: float, b: float) -> float:
    """Subtract second number from first with validation."""
    if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
        raise TypeError("Arguments must be numbers")
    return a - b


def multiply(a: float, b: float) -> float:
    """Multiply two numbers with validation."""
    if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
        raise TypeError("Arguments must be numbers")
    return a * b


def divide(a: float, b: float) -> float:
    """Divide first number by second with comprehensive error handling."""
    if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
        raise TypeError("Arguments must be numbers")
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b


def power(a: float, b: float) -> float:
    """Raise first number to the power of second."""
    if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
        raise TypeError("Arguments must be numbers")
    return a ** b


def sqrt(a: float) -> float:
    """Calculate square root with validation."""
    if not isinstance(a, (int, float)):
        raise TypeError("Argument must be a number")
    if a < 0:
        raise ValueError("Cannot calculate square root of negative number")
    return a ** 0.5
