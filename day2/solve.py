from enum import Enum
from functools import partial
from inputs import test_input, real_input
from typing import Generator, Callable


class Action(Enum):
    ROCK = 1
    PAPER = 2
    SCISSORS = 3

    def __lt__(self, other):
        if self == Action.ROCK:
            return other == Action.PAPER
        elif self == Action.PAPER:
            return other == Action.SCISSORS
        elif self == Action.SCISSORS:
            return other == Action.ROCK

    def how_to_lose(self) -> "Action":
        if self == Action.ROCK:
            return Action.SCISSORS
        elif self == Action.PAPER:
            return Action.ROCK
        elif self == Action.SCISSORS:
            return Action.PAPER

    def how_to_win(self) -> "Action":
        if self == Action.ROCK:
            return Action.PAPER
        elif self == Action.PAPER:
            return Action.SCISSORS
        elif self == Action.SCISSORS:
            return Action.ROCK


def strategy_for_part1(opponent: Action, unknown_parameter: str) -> Action:
    if unknown_parameter == "X":
        return Action.ROCK
    elif unknown_parameter == "Y":
        return Action.PAPER
    elif unknown_parameter == "Z":
        return Action.SCISSORS


def strategy_for_part2(opponent: Action, unknown_parameter: str) -> Action:
    if unknown_parameter == "X":
        return opponent.how_to_lose()
    elif unknown_parameter == "Y":
        return opponent
    elif unknown_parameter == "Z":
        return opponent.how_to_win()


class Round:
    opponent: Action
    you: Action

    def __init__(
        self,
        raw_opponent: str,
        unknown_parameter: str,
        strategy: Callable[[Action, str], Action],
    ) -> None:
        if raw_opponent == "A":
            self.opponent = Action.ROCK
        elif raw_opponent == "B":
            self.opponent = Action.PAPER
        elif raw_opponent == "C":
            self.opponent = Action.SCISSORS

        self.you = strategy(self.opponent, unknown_parameter)

    def __str__(self) -> str:
        return f"{self.opponent} vs. {self.you} ({self.result()})"

    def result(self) -> int:
        outcome = 0

        if self.you == self.opponent:
            outcome = 3
        elif self.you < self.opponent:
            outcome = 0
        elif self.you > self.opponent:
            outcome = 6

        return self.you.value + outcome


def strategy_guide_parser(
    raw_strategy_guide: str, strategy: Callable[[Action, str], Action]
) -> Generator[Round, None, None]:
    for raw_round in raw_strategy_guide.split("\n"):
        yield Round(*raw_round.split(), strategy=strategy)


def solve(
    raw_strategy_guide: str,
    parse_strategy_guide: Callable[[str], Generator[Round, None, None]],
) -> int:
    total_score = 0

    for round in parse_strategy_guide(raw_strategy_guide):
        total_score += round.result()

    return total_score


if __name__ == "__main__":
    total_score_part1 = solve(real_input, partial(strategy_guide_parser, strategy=strategy_for_part1))
    print(f"{total_score_part1=}")

    total_score_part2 = solve(real_input, partial(strategy_guide_parser, strategy=strategy_for_part2))
    print(f"{total_score_part2=}")
