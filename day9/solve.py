from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import Generator
from inputs import test_input, real_input


def direction(distance: int) -> int:
    if distance < 0:
        return -1
    elif distance == 0:
        return 0
    else:
        return 1


class Direction(Enum):
    LEFT = "L"
    RIGHT = "R"
    UP = "U"
    DOWN = "D"


@dataclass
class Move:
    direction: Direction
    steps: int

    def __init__(self, raw_move: str) -> None:
        raw_direction, raw_steps = raw_move.split()
        self.direction = Direction(raw_direction)
        self.steps = int(raw_steps)


@dataclass(unsafe_hash=True)
class Position:
    x: int = field(default=0)
    y: int = field(default=0)

    def copy(self) -> Position:
        return Position(x=self.x, y=self.y)

    def apply(self, move: Move) -> None:
        if move.direction == Direction.LEFT:
            self.x -= move.steps
        elif move.direction == Direction.RIGHT:
            self.x += move.steps
        elif move.direction == Direction.UP:
            self.y += move.steps
        elif move.direction == Direction.DOWN:
            self.y -= move.steps

    def follow(self, other: Position) -> Generator[Position, None, None]:
        dx = other.x - self.x
        dy = other.y - self.y

        yield self.copy()

        # Diagonaly steps
        while dx != 0 and dy != 0 and (abs(dx) + abs(dy)) > 2:
            self.x += direction(dx)
            self.y += direction(dy)
            dx -= direction(dx)
            dy -= direction(dy)
            yield self.copy()

        # Steps along x axis
        while abs(dx) > 1:
            self.x += direction(dx)
            dx -= direction(dx)
            yield self.copy()

        # Steps along y axis
        while abs(dy) > 1:
            self.y += direction(dy)
            dy -= direction(dy)
            yield self.copy()


@dataclass
class World:
    head: Position = field(init=False, default_factory=Position)
    tail: Position = field(init=False, default_factory=Position)
    visited: set[Position] = field(default_factory=set)

    def apply(self, move: Move) -> None:
        self.head.apply(move)
        self.visited.update(self.tail.follow(self.head))


def parse_moves(raw_moves: str) -> Generator[Move, None, None]:
    for raw_move in raw_moves.split("\n"):
        yield Move(raw_move)


def solve(moves: Generator[Move, None, None]) -> int:
    world = World()

    for move in moves:
        world.apply(move)

    return len(world.visited)


if __name__ == "__main__":
    visited_positions = solve(parse_moves(real_input))
    print(f"{visited_positions = }")
