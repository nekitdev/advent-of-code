from __future__ import annotations

from typing import Generic, List, Tuple, TypeVar

from attrs import frozen
from iters import iter
from iters.utils import unpack_binary
from orderings import LenientOrdered

from advent_of_code.common import solution, split_lines

T = TypeVar("T", bound=LenientOrdered)


@frozen()
class Range(Generic[T]):  # inclusive range
    start: T
    stop: T

    def contains(self, other: Range[T]) -> bool:
        return other.start >= self.start and other.stop <= self.stop

    __contains__ = contains

    def overlaps(self, other: Range[T]) -> bool:
        return other.start <= self.stop and other.stop >= self.start


Ranges = Tuple[Range[T], Range[T]]


def check_contains(left: Range[T], right: Range[T]) -> bool:
    return left in right or right in left


def check_overlaps(left: Range[T], right: Range[T]) -> bool:
    return left.overlaps(right)


COMMA = ","
DASH = "-"


def parse_ranges(string: str) -> Ranges[int]:
    left, right = string.split(COMMA)

    left_start, left_stop = map(int, left.split(DASH))
    right_start, right_stop = map(int, right.split(DASH))

    return (Range(left_start, left_stop), Range(right_start, right_stop))


def parse(source: str) -> List[Ranges[int]]:
    return iter(split_lines(source.strip())).map(parse_ranges).list()


def solve_part_one(data: List[Ranges[int]]) -> int:
    return iter(data).filter(unpack_binary(check_contains)).length()


def solve_part_two(data: List[Ranges[int]]) -> int:
    return iter(data).filter(unpack_binary(check_overlaps)).length()


solution(__name__, __file__)(parse, solve_part_one, solve_part_two)
