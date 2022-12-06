from typing import List

from iters import iter

from advent_of_code.common import solution

NEW_LINE = "\n"

DOUBLE_NEW_LINE = NEW_LINE + NEW_LINE


def split_new_line(string: str) -> List[str]:
    return string.split(NEW_LINE)


def split_double_new_line(string: str) -> List[str]:
    return string.split(DOUBLE_NEW_LINE)


def parse_section(section: List[str]) -> int:
    return iter(section).map(int).sum()


def parse(source: str) -> List[int]:
    return iter(split_double_new_line(source.strip())).map(split_new_line).map(parse_section).list()


def solve_part_one(data: List[int]) -> int:
    return iter(data).max()


COUNT = 3


def solve_part_two(data: List[int], count: int = COUNT) -> int:
    return iter(data).sort_reverse().take(count).sum()


solution(__name__, __file__)(parse, solve_part_one, solve_part_two)
