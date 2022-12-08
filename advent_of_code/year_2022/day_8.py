from typing import List, Tuple, TypeVar

from iters import iter
from iters.utils import unpack_ternary

from advent_of_code.common import Grid, Predicate, Ternary, enumerate_grid, grid_views, solution

T = TypeVar("T")

View = List[T]

Views = Tuple[View[T], View[T], View[T], View[T]]  # left, right, up, down

Point = Tuple[T, T]


split_lines = str.splitlines


def parse_row(row: str) -> List[int]:
    return iter(row).map(int).list()


def parse(source: str) -> Grid[int]:
    return iter(split_lines(source.strip())).map(parse_row).list()


def is_visible(height: int, views: Views[int]) -> bool:
    return iter(views).any_by(height_is_visible_on_view(height))


def is_visible_on_view(height: int, view: View[int]) -> bool:
    option = iter(view).max_or_none()

    return option is None or height > option


def height_is_visible_on_view(height: int) -> Predicate[View[int]]:
    def predicate(view: View[int]) -> bool:
        return is_visible_on_view(height, view)

    return predicate


def count_score(height: int, views: Views[int]) -> int:
    score = 1

    for view in views:
        sub_score = 0

        for other in view:
            if other < height:
                sub_score += 1

            else:
                sub_score += 1
                break

        score *= sub_score

    return score


def count_score_for_grid_views(grid: Grid[int]) -> Ternary[int, int, int, int]:
    def ternary(x: int, y: int, height: int) -> int:
        return count_score(height, grid_views(grid, x, y))

    return ternary


def is_visible_for_grid_views(grid: Grid[int]) -> Ternary[int, int, int, bool]:
    def ternary(x: int, y: int, height: int) -> bool:
        return is_visible(height, grid_views(grid, x, y))

    return ternary


def solve_part_one(data: List[List[int]]) -> int:
    return iter(enumerate_grid(data)).map(unpack_ternary(is_visible_for_grid_views(data))).sum()


def solve_part_two(data: List[List[int]]) -> int:
    return iter(enumerate_grid(data)).map(unpack_ternary(count_score_for_grid_views(data))).max()


solution(__name__, __file__)(parse, solve_part_one, solve_part_two)
