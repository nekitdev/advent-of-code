from enum import Enum
from typing import List, Tuple

from attrs import define, frozen
from iters import iter

from advent_of_code.common import solution, split_lines


@frozen()
class Point:
    x: int = 0
    y: int = 0


@define()
class Knot:
    x: int = 0
    y: int = 0

    def into_point(self) -> Point:
        return Point(self.x, self.y)


Knots = List[Knot]


class Direction(Enum):
    UP = "U"
    DOWN = "D"
    LEFT = "L"
    RIGHT = "R"


DirectionWithLength = Tuple[Direction, int]
DirectionsWithLength = List[DirectionWithLength]


def parse_line(line: str) -> DirectionWithLength:
    direction, length = line.split()
    return (Direction(direction), int(length))


def parse(source: str) -> DirectionsWithLength:
    return iter(split_lines(source.strip())).map(parse_line).list()


UNKNOWN_DIRECTION = "unknown direction: `{}`"


def move_head(head: Knot, direction: Direction) -> None:
    if direction is Direction.RIGHT:
        head.x += 1

    elif direction is Direction.LEFT:
        head.x -= 1

    elif direction is Direction.UP:
        head.y += 1

    elif direction is Direction.DOWN:
        head.y -= 1

    else:
        raise ValueError(UNKNOWN_DIRECTION.format(direction))


def move_knot(knot: Knot, previous: Knot) -> None:
    dx = previous.x - knot.x
    dy = previous.y - knot.y

    if dy > 1:
        knot.y += 1

        if dx > 0:
            knot.x += 1

        elif dx < 0:
            knot.x -= 1

    elif dy < -1:
        knot.y -= 1

        if dx > 0:
            knot.x += 1

        elif dx < 0:
            knot.x -= 1

    elif dx > 1:
        knot.x += 1

        if dy > 0:
            knot.y += 1

        elif dy < 0:
            knot.y -= 1

    elif dx < -1:
        knot.x -= 1

        if dy > 0:
            knot.y += 1

        elif dy < 0:
            knot.y -= 1


def solve_knots(data: DirectionsWithLength, knots: Knots) -> int:
    tail_visited = {Point()}

    head, *knots = knots

    for direction, length in data:
        for _ in range(length):
            previous = head

            move_head(head, direction)

            for knot in knots:
                move_knot(knot, previous)

                previous = knot

            tail_visited.add(previous.into_point())  # last `previous` is the tail

    return len(tail_visited)


def generate_knots(count: int) -> List[Knot]:
    return iter.repeat_exactly_with(Knot, count).list()


COUNT_ONE = 2
COUNT_TWO = 10


def solve_part_one(data: DirectionsWithLength) -> int:
    return solve_knots(data, generate_knots(COUNT_ONE))


def solve_part_two(data: DirectionsWithLength) -> int:
    return solve_knots(data, generate_knots(COUNT_TWO))


solution(__name__, __file__)(parse, solve_part_one, solve_part_two)
