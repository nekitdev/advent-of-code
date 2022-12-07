from typing import List, Tuple

from iters import iter
from iters.utils import unpack_binary, unpack_ternary

from advent_of_code.common import solution, split_lines

PRIORITY_LINE = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
PRIORITY = {letter: priority for priority, letter in iter(PRIORITY_LINE).enumerate_from(1).unwrap()}


def priority(letter: str) -> int:
    return PRIORITY[letter]


def divide(string: str) -> Tuple[str, str]:
    middle = len(string) // 2

    return (string[:middle], string[middle:])


def parse(source: str) -> List[str]:
    return split_lines(source.strip())


def find_item_priority(left: str, right: str) -> int:
    return priority((set(left) & set(right)).pop())


def find_group_item_priority(left: str, middle: str, right: str) -> int:
    return priority((set(left) & set(middle) & set(right)).pop())


def solve_part_one(data: List[str]) -> int:
    return iter(data).map(divide).map(unpack_binary(find_item_priority)).sum()


def solve_part_two(data: List[str]) -> int:
    return iter(data).groups(3).map(unpack_ternary(find_group_item_priority)).sum()


solution(__name__, __file__)(parse, solve_part_one, solve_part_two)
