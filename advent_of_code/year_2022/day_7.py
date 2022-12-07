from __future__ import annotations

from functools import lru_cache
from typing import Iterator, List, Optional, Sequence, TypeVar, Union

from attrs import field, frozen
from typing_extensions import Literal, TypeGuard

from advent_of_code.common import Predicate, solution, split_lines

CAN_NOT_FIND = "can not find `{}`"

cache = lru_cache(None)


@frozen()
class Directory:
    name: str = field()

    parent: Optional[Directory] = field(default=None)

    children: List[Item] = field(factory=list)

    def find_by_name(self, name: str) -> Item:
        for child in self.children:
            if child.name == name:
                return child

        raise FileNotFoundError(CAN_NOT_FIND.format(name))

    def is_directory(self) -> Literal[True]:
        return True

    def is_file(self) -> Literal[False]:
        return False

    @property
    def size(self) -> int:
        return sum(child.size for child in self.children)


@frozen()
class File:
    name: str = field()
    size: int = field()

    directory: Directory = field()

    def is_directory(self) -> Literal[False]:
        return False

    def is_file(self) -> Literal[True]:
        return True


Item = Union[Directory, File]

ROOT = "/"
DOTS = ".."

COMMAND = "$"

DIR = "dir"

LS = "ls"


FIRST = 0

T = TypeVar("T")


def first(sequence: Sequence[T]) -> T:
    return sequence[FIRST]


CAN_NOT_CHANGE = "can not change directory with `..` without `parent` present"

CAN_NOT_CHANGE_TO_FILE = "can not change directory to file"


def parse(source: str) -> Directory:
    root = Directory(ROOT)

    current = root

    for line in split_lines(source.strip()):
        head, *tail = line.split()

        if head == COMMAND:
            command, *arguments = tail

            if command == LS:
                continue

            name = first(arguments)

            if name == ROOT:
                current = root

            elif name == DOTS:
                parent = current.parent

                if parent is None:
                    raise FileNotFoundError(CAN_NOT_CHANGE)

                current = parent

            else:
                child = current.find_by_name(name)

                if is_directory(child):
                    current = child

                else:
                    raise NotADirectoryError(CAN_NOT_CHANGE_TO_FILE)

        else:
            name = first(tail)

            if head == DIR:
                child = Directory(name, current)

                current.children.append(child)

            else:
                size = int(head)

                child = File(name, size, current)

                current.children.append(child)

    return root


THRESHOLD = 100_000


def is_directory(item: Item) -> TypeGuard[Directory]:
    return item.is_directory()


def is_file(item: Item) -> TypeGuard[File]:
    return item.is_file()


def size_less_or_equal(threshold: int) -> Predicate[Directory]:
    def less_or_equal(directory: Directory) -> bool:
        return directory.size <= threshold

    return less_or_equal


def size_greater_or_equal(to_remove: int) -> Predicate[Directory]:
    def greater_or_equal(directory: Directory) -> bool:
        return directory.size >= to_remove

    return greater_or_equal


def find_directories(predicate: Predicate[Directory], node: Directory) -> Iterator[Directory]:
    if predicate(node):
        yield node

    for child in node.children:
        if is_directory(child):
            yield from find_directories(predicate, child)


def solve_part_one(data: Directory, threshold: int = THRESHOLD) -> int:
    return sum(
        directory.size for directory in find_directories(size_less_or_equal(threshold), data)
    )


TOTAL = 70_000_000
NEEDED = 30_000_000
ALLOWED = TOTAL - NEEDED
DEFAULT = 0


def solve_part_two(data: Directory, allowed: int = ALLOWED, default: int = DEFAULT) -> int:
    to_remove = data.size - allowed

    return min(
        (directory.size for directory in find_directories(size_greater_or_equal(to_remove), data)),
        default=default,
    )


solution(__name__, __file__)(parse, solve_part_one, solve_part_two)
