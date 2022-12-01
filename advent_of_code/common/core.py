from pathlib import Path
from typing import Callable, TypeVar, Union, overload

from entrypoint import entrypoint
from typing_extensions import Literal

__all__ = ("source_path", "solution")

D = TypeVar("D")
T = TypeVar("T")
U = TypeVar("U")
V = TypeVar("V")
R = TypeVar("R")

Unary = Callable[[T], R]
Binary = Callable[[T, U], R]
Ternary = Callable[[T, U, V], R]

Parse = Unary[str, D]
Solve = Unary[D, T]

SolveOnly = Binary[Parse[D], Solve[D, T], None]
SolveBoth = Ternary[Parse[D], Solve[D, T], Solve[D, T], None]
SolveAny = Union[SolveOnly[D, T], SolveBoth[D, T]]

SOURCE_SUFFIX = ".in"


def source_path(path: str, suffix: str = SOURCE_SUFFIX) -> Path:
    return Path(path).with_suffix(suffix)


ONLY = False


@overload
def solution(name: str, path: str, only: Literal[False] = ...) -> SolveBoth[D, T]:
    ...


@overload
def solution(name: str, path: str, only: Literal[True]) -> SolveOnly[D, T]:
    ...


def solution(name: str, path: str, only: bool = ONLY) -> SolveAny[D, T]:
    if only:
        def solve_only(parse: Parse[D], solve_only: Solve[D, T]) -> None:
            @entrypoint(name)
            def _() -> None:
                with source_path(path).open() as file:
                    data = parse(file.read())

                print(solve_only(data))

        return solve_only

    else:
        def solve_both(
            parse: Parse[D], solve_part_one: Solve[D, T], solve_part_two: Solve[D, T]
        ) -> None:
            @entrypoint(name)
            def _() -> None:
                with source_path(path).open() as file:
                    data = parse(file.read())

                print(solve_part_one(data))
                print(solve_part_two(data))

        return solve_both
