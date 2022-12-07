from pathlib import Path
from typing import TypeVar, Union, overload

from entrypoint import entrypoint
from typing_extensions import Literal

from advent_of_code.common.timer import create_timer
from advent_of_code.common.typing import Binary, Ternary, Unary

__all__ = ("source_path", "solution")

D = TypeVar("D")
T = TypeVar("T")

Parse = Unary[str, D]
Solve = Unary[D, T]

SolveOnly = Binary[Parse[D], Solve[D, T], None]
SolveBoth = Ternary[Parse[D], Solve[D, T], Solve[D, T], None]
SolveAny = Union[SolveOnly[D, T], SolveBoth[D, T]]

SOURCE_SUFFIX = ".in"


def source_path(path: str, suffix: str = SOURCE_SUFFIX) -> Path:
    return Path(path).with_suffix(suffix)


ONLY = False

SOURCE = "read source in `{}`"
SOLVED_ONLY = "solved in `{}`"
SOLVED_ONE = "solved part one in `{}`"
SOLVED_TWO = "solved part two in `{}`"


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
                timer = create_timer()

                with source_path(path).open() as file:
                    data = parse(file.read())

                print(SOURCE.format(timer.elapsed()))

                timer = timer.reset()

                print(solve_only(data))

                print(SOLVED_ONLY.format(timer.elapsed()))

        return solve_only

    else:

        def solve_both(
            parse: Parse[D], solve_part_one: Solve[D, T], solve_part_two: Solve[D, T]
        ) -> None:
            @entrypoint(name)
            def _() -> None:
                timer = create_timer()

                with source_path(path).open() as file:
                    data = parse(file.read())

                print(SOURCE.format(timer.elapsed()))

                timer = timer.reset()

                print(solve_part_one(data))

                print(SOLVED_ONE.format(timer.elapsed()))

                timer = timer.reset()

                print(solve_part_two(data))

                print(SOLVED_TWO.format(timer.elapsed()))

        return solve_both
