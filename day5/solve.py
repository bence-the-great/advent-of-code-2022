from collections import deque
import re
from typing import Generator, Callable
from inputs import test_input, real_input


class Move:
    number_of_crates: int
    origin: int
    destination: int

    def __init__(self, raw_move: str) -> None:
        regex = "move\s(?P<number_of_crates>[\d]*)\sfrom\s(?P<origin>[\d]*)\sto\s(?P<destination>[\d]*)"
        self.number_of_crates, self.origin, self.destination = map(int, re.findall(regex, raw_move)[0])
        self.origin -= 1
        self.destination -= 1

    def __str__(self) -> str:
        return f"#{self.number_of_crates} ({self.origin+1} -> {self.destination+1})"


class Stacks(list):
    apply_move_function: Callable[[Move], None]

    def __init__(self, apply_move_function: Callable[["Stacks", Move], None]) -> None:
        self.apply_move_function = apply_move_function

    def parse(self, raw_stacks: str):
        for raw_line in raw_stacks.split("\n"):
            self._parse_line(raw_line)

    def _parse_line(self, raw_line: str) -> list[str]:
        position = 0

        while position < len(raw_line):
            char = raw_line[position]

            if char == "[":
                self[int(position / 4)].append(raw_line[position + 1])
                position += 3

            position += 1

    def _create_missing(self, index: int) -> None:
        for _ in range(len(self), index + 1):
            self.append(deque())

    def __getitem__(self, index: int) -> list[str]:
        if len(self) <= index:
            self._create_missing(index)

        return super().__getitem__(index)

    def apply(self, move: Move) -> None:
        self.apply_move_function(self, move)

    def top_elements(self) -> list[str]:
        return [stack[0] for stack in self]


def moves(raw_moves: str) -> Generator[Move, None, None]:
    for raw_move in raw_moves.split("\n"):
        yield Move(raw_move)


def apply_move_crate_mover_9000(self: Stacks, move: Move):
    for _ in range(move.number_of_crates):
        self[move.destination].appendleft(self[move.origin].popleft())


def apply_move_crate_mover_9001(self: Stacks, move: Move):
    crates_picked_up = [self[move.origin].popleft() for _ in range(move.number_of_crates)]
    self[move.destination].extendleft(reversed(crates_picked_up))


def solve(raw_crate_rearrangements: str, stacks: Stacks) -> str:
    raw_stacks, raw_moves = raw_crate_rearrangements.split("\n\n")

    stacks.parse(raw_stacks)

    for move in moves(raw_moves):
        stacks.apply(move)

    return "".join(stacks.top_elements())


if __name__ == "__main__":
    solution_part1 = solve(real_input, Stacks(apply_move_crate_mover_9000))
    print(f"{solution_part1 = }")
    solution_part2 = solve(real_input, Stacks(apply_move_crate_mover_9001))
    print(f"{solution_part2 = }")
