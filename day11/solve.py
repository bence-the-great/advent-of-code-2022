from __future__ import annotations
from collections import deque
from dataclasses import dataclass, field
import re
from typing import Callable
from inputs import test_input, real_input

OPERATION_REGEX = re.compile(r"\s*Operation:\s*new\s*=\s*old\s*(?P<operator>[*+])\s*(?P<value>(old|\d+))\s*")
STARTING_ITEMS_REGEX = re.compile(r"(?P<item>\d+)")
TEST_REGEXES = {
    "value": re.compile(r"divisible\s*by\s*(?P<value>[-+]?[\d]*)"),
    "throw_to": re.compile(r"(?P<outcome>(true|false)): throw to monkey\s*(?P<value>[\d]+)"),
}


@dataclass
class Easing:
    value: int

    def ease(self, old_worry_level: int) -> int:
        return int(old_worry_level / self.value)


@dataclass
class Operation:
    def inspect(self, old_worry_level: int) -> int:
        raise NotImplementedError


@dataclass
class OperationAdd(Operation):
    value: int

    def inspect(self, old_worry_level: int) -> int:
        return old_worry_level + self.value


@dataclass
class OperationMultiply(Operation):
    value: int

    def inspect(self, old_worry_level: int) -> int:
        return old_worry_level * self.value


@dataclass
class OperationSquare(Operation):
    def inspect(self, old_worry_level: int) -> int:
        return old_worry_level * old_worry_level


@dataclass
class MonkeyTest:
    value: int
    if_true: int
    if_false: int

    def throw_to(self, worry_level: int) -> int:
        raise NotImplementedError


@dataclass
class MonkeyTestDivisible(MonkeyTest):
    def throw_to(self, worry_level: int) -> int:
        if worry_level % self.value == 0:
            return self.if_true
        else:
            return self.if_false


@dataclass
class Monkey:
    items: deque[int]
    inspected_number_of_items: int = field(init=False, default=0)
    monkeys: list[Monkey]
    operation: Operation
    test: MonkeyTest
    ease: Callable[[int], int]

    def __lt__(self, other: Monkey) -> bool:
        return self.inspected_number_of_items < other.inspected_number_of_items

    def __gt__(self, other: Monkey) -> bool:
        return self.inspected_number_of_items > other.inspected_number_of_items

    def inspect_items(self) -> None:
        for _ in range(len(self.items)):
            item = self.ease(self.operation.inspect(self.items.popleft()))
            self.monkeys[self.test.throw_to(item)].items.append(item)
            self.inspected_number_of_items += 1


def parse_starting_items(raw_starting_items: str) -> deque[int]:
    matches = STARTING_ITEMS_REGEX.finditer(raw_starting_items)
    return deque(int(match.groupdict()["item"]) for match in matches)


def parse_operation(raw_operation: str) -> Operation:
    extracted_data = list(OPERATION_REGEX.finditer(raw_operation))[0].groupdict()

    raw_value = extracted_data["value"]

    if extracted_data["operator"] == "+":
        return OperationAdd(value=int(raw_value))
    elif extracted_data["operator"] == "*":
        if raw_value == "old":
            return OperationSquare()
        else:
            return OperationMultiply(value=int(raw_value))
    else:
        raise ValueError(f"unexpected operator {extracted_data['operator']}")


def parse_test(raw_test: str) -> MonkeyTest:
    extracted_value = int(list(TEST_REGEXES["value"].finditer(raw_test))[0].groupdict()["value"])
    extracted_outcomes = (match.groupdict() for match in TEST_REGEXES["throw_to"].finditer(raw_test))

    if extracted_value == 0:
        raise ValueError(f"divisible by cannot be {extracted_value}")

    return MonkeyTestDivisible(
        value=extracted_value,
        **{f"if_{match['outcome']}": int(match["value"]) for match in extracted_outcomes},
    )


def parse_monkeys(raw_monkeys: str) -> list[Monkey]:
    easing_function = lambda item: int(item / 3)
    monkeys = []
    lines = raw_monkeys.splitlines()
    current_line_no = 0
    num_lines = len(lines)

    while current_line_no < num_lines:
        current_line = lines[current_line_no]

        if current_line.startswith("Monkey"):
            starting_items = parse_starting_items(lines[current_line_no + 1])
            operation = parse_operation(lines[current_line_no + 2])
            monkey_test = parse_test("\n".join(lines[current_line_no + 3 : current_line_no + 6]))

            monkeys.append(
                Monkey(
                    items=starting_items, monkeys=monkeys, operation=operation, test=monkey_test, ease=easing_function
                )
            )
            current_line_no += 7
        else:
            current_line_no += 1

    return monkeys


def solve(monkeys: list[Monkey], rounds: int) -> int:
    for _ in range(rounds):
        for monkey in monkeys:
            monkey.inspect_items()

    busiest_2_monkeys = sorted(monkeys, reverse=True)[:2]

    return busiest_2_monkeys[0].inspected_number_of_items * busiest_2_monkeys[1].inspected_number_of_items


if __name__ == "__main__":
    monkey_business = solve(parse_monkeys(real_input), rounds=20)
    print(f"{monkey_business = }")
