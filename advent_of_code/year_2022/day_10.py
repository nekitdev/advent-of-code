from abc import abstractmethod
from typing import List

from attrs import define, frozen
from iters import iter
from typing_extensions import Protocol

from advent_of_code.common import solution, split_lines

INITIAL_X = 1
INITIAL_CYCLE = 0
INITIAL_STRENGTHS = 0

INTERRUPT_DIVISOR = 40

INTERRUPTS = frozenset((20, 60, 100, 140, 180, 220))

EMPTY = str()

NEW_LINE = "\n"
GLYPH = "█"
SPACE = " "


@define()
class Circuit:
    x: int = INITIAL_X

    cycle: int = INITIAL_CYCLE
    strengths: int = INITIAL_STRENGTHS
    output: str = EMPTY

    def interrupt(self) -> None:
        cycle = self.cycle
        x = self.x

        if cycle in INTERRUPTS:
            self.strengths += cycle * x

        whole, value = divmod(cycle, INTERRUPT_DIVISOR)

        value -= 1

        if not value and whole:
            self.output += NEW_LINE

        xs = {x - 1, x, x + 1}

        if value in xs:
            self.output += GLYPH

        else:
            self.output += SPACE

    def step(self) -> None:
        self.cycle += 1

        self.interrupt()


class Operation(Protocol):
    @abstractmethod
    def execute(self, circuit: Circuit) -> None:
        ...


Operations = List[Operation]


@frozen()
class NoOperation(Operation):
    def execute(self, circuit: Circuit) -> None:
        circuit.step()


@frozen()
class AddX(Operation):
    value: int

    def execute(self, circuit: Circuit) -> None:
        circuit.step()
        circuit.step()

        circuit.x += self.value


NOOP = "noop"
ADDX = "addx"

UNKNOWN_OPERATION = "unknown operation: `{}`"


def parse_operation(line: str) -> Operation:
    operation, *arguments = line.split()

    if operation == NOOP:
        return NoOperation()

    if operation == ADDX:
        (value,) = map(int, arguments)

        return AddX(value)

    raise SyntaxError(UNKNOWN_OPERATION.format(line))


def parse(source: str) -> Operations:
    return iter(split_lines(source.strip())).map(parse_operation).list()


def execute_operations(data: Operations) -> Circuit:
    circuit = Circuit()

    for operation in data:
        operation.execute(circuit)

    return circuit


def solve_part_one(data: Operations) -> int:
    return execute_operations(data).strengths


def solve_part_two(data: Operations) -> str:
    return execute_operations(data).output


solution(__name__, __file__)(parse, solve_part_one, solve_part_two)
