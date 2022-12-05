from functools import partial
from typing import DefaultDict, List, Sequence, TypeVar

from attrs import define, field, frozen
from iters import iter
from parse import Parser

from advent_of_code.common import solution

MOVE = "move {count:d} from {source_name} to {destination_name}"
BOX = "[{name}]"

COUNT = "count"
SOURCE_NAME = "source_name"
DESTINATION_NAME = "destination_name"

NAME = "name"

MOVE_PARSER = Parser(MOVE)
BOX_PARSER = Parser(BOX)


@frozen()
class Move:
    count: int
    source_name: str
    destination_name: str


Moves = List[Move]


@frozen()
class Box:
    name: str


Boxes = List[Box]


S = TypeVar("S", bound="Stack")


@define()
class Stack:
    boxes: Boxes = field(factory=list)

    def clone(self: S) -> S:
        return type(self)(self.boxes)


Stacks = DefaultDict[str, Stack]

default_stack_dict = partial(DefaultDict[str, Stack], Stack)


E = TypeVar("E", bound="Executor")


@frozen()
class Executor:
    stacks: Stacks = field(factory=default_stack_dict)
    moves: Moves = field(factory=list)

    def clone(self: E) -> E:
        stacks = default_stack_dict()

        stacks.update({name: stack.clone() for name, stack in self.stacks.items()})

        return type(self)(stacks, self.moves)

    def run(self, reverse: bool) -> None:
        stacks = self.stacks

        for move in self.moves:
            count = move.count

            source_name = move.source_name
            destination_name = move.destination_name

            source = stacks[source_name]
            destination = stacks[destination_name]

            to_add = source.boxes[:count]

            if reverse:
                to_add.reverse()

            destination.boxes = to_add + destination.boxes

            source.boxes = source.boxes[count:]


NEW_LINE = "\n"
DOUBLE_NEW_LINE = NEW_LINE + NEW_LINE
SPACE = " "


def split_new_line(string: str) -> List[str]:
    return string.split(NEW_LINE)


def split_double_new_line(string: str) -> List[str]:
    return string.split(DOUBLE_NEW_LINE)


def split_space(string: str) -> List[str]:
    return string.split(SPACE)


CAN_NOT_PARSE = "can not parse move `{}`"


def parse_move(string: str) -> Move:
    result = MOVE_PARSER.parse(string)

    if result is None:
        raise ValueError(CAN_NOT_PARSE.format(string))

    named = result.named

    return Move(named[COUNT], named[SOURCE_NAME], named[DESTINATION_NAME])


FACTOR = 4

Names = List[str]


def parse_boxes(stacks: Stacks, names: Names, line: str) -> None:
    index = 0

    factor = FACTOR

    box_parser = BOX_PARSER

    for string, group in iter(split_space(line)).group_list():
        if not string:
            index += len(group) // factor

        else:
            for string in group:
                result = box_parser.parse(string)

                box = Box(result.named[NAME])

                stacks[names[index]].boxes.append(box)

                index += 1


LAST = ~0


def parse(source: str) -> Executor:
    state_string, moves_string = split_double_new_line(source.strip())

    *lines, names_string = split_new_line(state_string)

    names = names_string.split()

    stacks = default_stack_dict()

    partial_parse_boxes = partial(parse_boxes, stacks, names)

    iter(lines).for_each(partial_parse_boxes)

    moves = iter(split_new_line(moves_string)).map(parse_move).list()

    return Executor(stacks, moves)


FIRST = 0

T = TypeVar("T")


def first(sequence: Sequence[T]) -> T:
    return sequence[FIRST]


EMPTY = str()
concat = EMPTY.join


def solve_part_one(data: Executor) -> str:
    executor = data.clone()

    executor.run(reverse=True)

    return concat(first(stack.boxes).name for stack in executor.stacks.values())


def solve_part_two(data: Executor) -> str:
    executor = data.clone()

    executor.run(reverse=False)

    return concat(first(stack.boxes).name for stack in executor.stacks.values())


solution(__name__, __file__)(parse, solve_part_one, solve_part_two)
