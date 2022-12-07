from typing import Callable, TypeVar

__all__ = ("Unary", "Binary", "Ternary", "Predicate")

T = TypeVar("T")
U = TypeVar("U")
V = TypeVar("V")
R = TypeVar("R")

Unary = Callable[[T], R]
Binary = Callable[[T, U], R]
Ternary = Callable[[T, U, V], R]

Predicate = Unary[T, bool]
