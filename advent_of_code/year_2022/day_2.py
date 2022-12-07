from enum import Enum
from typing import List, Tuple

from iters import iter
from iters.utils import unpack_binary

from advent_of_code.common import solution, split_lines

A = "A"
B = "B"
C = "C"

X = "X"
Y = "Y"
Z = "Z"


class Choice(Enum):
    ROCK = 1
    PAPER = 2
    SCISSORS = 3


COMPUTER = {A: Choice.ROCK, B: Choice.PAPER, C: Choice.SCISSORS}
PLAYER = {X: Choice.ROCK, Y: Choice.PAPER, Z: Choice.SCISSORS}


BEATS = {Choice.ROCK: Choice.SCISSORS, Choice.PAPER: Choice.ROCK, Choice.SCISSORS: Choice.PAPER}
BEATEN = {beaten: beats for beats, beaten in BEATS.items()}


class Result(Enum):
    LOSS = 0
    TIE = 3
    WIN = 6


RESULT = {X: Result.LOSS, Y: Result.TIE, Z: Result.WIN}


def compare(computer_choice: Choice, player_choice: Choice) -> Result:
    if computer_choice is player_choice:
        return Result.TIE

    if BEATS[computer_choice] is player_choice:
        return Result.LOSS

    return Result.WIN


def compute_choice(computer_choice: Choice, result: Result) -> Choice:
    if result is Result.TIE:
        return computer_choice

    if result is Result.LOSS:
        return BEATS[computer_choice]

    return BEATEN[computer_choice]


def compute_score(computer_choice: Choice, player_choice: Choice) -> int:
    return compare(computer_choice, player_choice).value + player_choice.value


def compute_choice_score(computer_choice: Choice, result: Result) -> int:
    return compute_choice(computer_choice, result).value + result.value


def parse_section(string: str) -> Tuple[str, str]:
    left, right = string.split()

    return (left, right)


def parse(source: str) -> List[Tuple[str, str]]:
    return iter(split_lines(source.strip())).map(parse_section).list()


def get_choices(item: Tuple[str, str]) -> Tuple[Choice, Choice]:
    computer, player = item

    return (COMPUTER[computer], PLAYER[player])


def get_choice_and_result(item: Tuple[str, str]) -> Tuple[Choice, Result]:
    computer, result = item

    return (COMPUTER[computer], RESULT[result])


def solve_part_one(data: List[Tuple[str, str]]) -> int:
    return iter(data).map(get_choices).map(unpack_binary(compute_score)).sum()


def solve_part_two(data: List[Tuple[str, str]]) -> int:
    return iter(data).map(get_choice_and_result).map(unpack_binary(compute_choice_score)).sum()


solution(__name__, __file__)(parse, solve_part_one, solve_part_two)
