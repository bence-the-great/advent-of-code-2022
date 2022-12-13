from __future__ import annotations
from dataclasses import dataclass, field
from functools import partial
from typing import Generator, Callable
from inputs import test_input, real_input

TOTAL_DISK_SPACE = 70_000_000
REQUIRED_UNUSED_SPACE = 30_000_000


@dataclass(frozen=True)
class File:
    name: str
    size: int
    parent: Directory


@dataclass(frozen=True)
class Directory:
    name: str
    parent: Directory | None
    contents: list[Directory | File] = field(default_factory=list)

    def append(self, item: str) -> None:
        if item.startswith("dir"):
            size, directory_name = item.split()
            self.contents.append(Directory(name=directory_name, parent=self))
        else:
            size, filename = item.split()
            self.contents.append(File(name=filename, size=int(size), parent=self))

    def __getitem__(self, __name: str) -> Directory | File:
        if __name == "..":
            return self.parent
        for item in self.contents:
            if item.name == __name:
                return item
        raise KeyError(f'No such file or directory as "{__name}".')

    @property
    def size(self) -> int:
        return sum((c.size for c in self.contents))

    @property
    def directories(self) -> Generator[Directory, None, None]:
        return (d for d in self.contents if isinstance(d, Directory))


def parse_console_output(console_output: str) -> Directory:
    root_directory = Directory(name="/", parent=None)
    current_directory = None
    for line in console_output.split("\n"):
        if line.startswith("$"):
            command = line[2:]
            if command.startswith("cd"):
                location = command[3:]
                if location == "/":
                    current_directory = root_directory
                else:
                    current_directory = current_directory[location]
        else:
            current_directory.append(line)

    return root_directory


def collect_directories(
    parent_directory: Directory, condition: Callable[[Directory], bool]
) -> Generator[Directory, None, None]:
    for directory in parent_directory.directories:
        yield from collect_directories(directory, condition)
    if condition(parent_directory):
        yield parent_directory


def size_is_at_most_n(directory: Directory, n: int) -> bool:
    return directory.size <= n


def size_is_at_least_n(directory: Directory, n: int) -> bool:
    return directory.size >= n


def part1(root_directory: Directory) -> int:
    return sum(map(lambda d: d.size, collect_directories(root_directory, partial(size_is_at_most_n, n=100_000))))


def part2(root_directory: Directory) -> int:
    need_to_free = REQUIRED_UNUSED_SPACE - (TOTAL_DISK_SPACE - root_directory.size)
    return min(map(lambda d: d.size, collect_directories(root_directory, partial(size_is_at_least_n, n=need_to_free))))


if __name__ == "__main__":
    root_directory = parse_console_output(real_input)

    size = part1(root_directory)
    print(f"{size = }")

    directory_to_delete = part2(root_directory)
    print(f"{directory_to_delete = }")
