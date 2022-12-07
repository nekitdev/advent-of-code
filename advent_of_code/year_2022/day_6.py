from typing import Sized

from iters import iter

from advent_of_code.common import Predicate, solution


START_OF_PACKET_COUNT = 4
START_OF_MESSAGE_COUNT = 14


def parse(source: str) -> str:
    return source


def is_start_of(count: int) -> Predicate[Sized]:
    def predicate(data: Sized) -> bool:
        return len(data) == count

    return predicate


def find_count(count: int, data: str) -> int:
    return iter(data).set_windows(count).position(is_start_of(count)) + count


def solve_part_one(data: str) -> int:
    return find_count(START_OF_PACKET_COUNT, data)


def solve_part_two(data: str) -> int:
    return find_count(START_OF_MESSAGE_COUNT, data)


solution(__name__, __file__)(parse, solve_part_one, solve_part_two)
