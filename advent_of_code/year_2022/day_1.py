from typing import List

from iters import iter

from advent_of_code.common import solution, split_double_lines, split_lines


def parse_section(section: List[str]) -> int:
    return iter(section).map(int).sum()


def parse(source: str) -> List[int]:
    return iter(split_double_lines(source.strip())).map(split_lines).map(parse_section).list()


def solve_part_one(data: List[int]) -> int:
    return iter(data).max()


COUNT = 3


def solve_part_two(data: List[int], count: int = COUNT) -> int:
    return iter(data).sort_reverse().take(count).sum()


solution(__name__, __file__)(parse, solve_part_one, solve_part_two)
