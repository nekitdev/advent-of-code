from typing import Callable, List, Tuple, TypeVar

__all__ = ("Unary", "Binary", "Ternary", "Predicate", "Grid", "GridView", "GridViews")

T = TypeVar("T")
U = TypeVar("U")
V = TypeVar("V")
R = TypeVar("R")

Unary = Callable[[T], R]
Binary = Callable[[T, U], R]
Ternary = Callable[[T, U, V], R]

Predicate = Unary[T, bool]

Grid = List[List[T]]

GridView = List[T]
GridViews = Tuple[GridView[T], GridView[T], GridView[T], GridView[T]]  # left, right, up, down
