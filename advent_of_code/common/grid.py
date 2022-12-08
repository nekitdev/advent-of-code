from typing import Iterator, Tuple, TypeVar

from advent_of_code.common.typing import Grid, GridViews

__all__ = ("enumerate_grid", "grid_views")

T = TypeVar("T")


def enumerate_grid(grid: Grid[T]) -> Iterator[Tuple[int, int, T]]:
    for x, row in enumerate(grid):
        for y, item in enumerate(row):
            yield (x, y, item)


def grid_views(data: Grid[T], x: int, y: int) -> GridViews[T]:
    xs = x + 1
    ys = y + 1

    left = data[x][:y]

    left.reverse()

    right = data[x][ys:]

    up = [row[y] for row in data[:x]]

    up.reverse()

    down = [row[y] for row in data[xs:]]

    return (left, right, up, down)
