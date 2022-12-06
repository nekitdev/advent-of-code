from functools import partial
from typing import Set, TypeVar

from iters import iter

from advent_of_code.common import solution

T = TypeVar("T")

START_OF_PACKET_COUNT = 4
START_OF_MESSAGE_COUNT = 14


def parse(source: str) -> str:
    return source


def is_start_of(count: int, data: Set[str]) -> bool:
    return len(data) == count


def find_count(count: int, data: str) -> int:
    is_start = partial(is_start_of, count)

    return iter(data).set_windows(count).position(is_start) + count


def solve_part_one(data: str) -> int:
    return find_count(START_OF_PACKET_COUNT, data)


def solve_part_two(data: str) -> int:
    return find_count(START_OF_MESSAGE_COUNT, data)


solution(__name__, __file__)(parse, solve_part_one, solve_part_two)
