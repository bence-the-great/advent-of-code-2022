from typing import Generator
from inputs import test_input, real_input


def get_priority(item: str) -> int:
    if ord("A") <= ord(item) <= ord("Z"):
        return ord(item) - 38
    elif ord("a") <= ord(item) <= ord("z"):
        return ord(item) - 96
    else:
        return 0


def solve_part1(raw_rucksacks: str) -> int:
    sum_of_priorities = 0

    for rucksack in raw_rucksacks.split("\n"):
        divider = int(len(rucksack) / 2)
        common_items = set(rucksack[:divider]) & set(rucksack[divider:])
        for item in common_items:
            sum_of_priorities += get_priority(item)

    return sum_of_priorities


def rucksack_groups(raw_rucksacks: str) -> Generator[list[str], None, None]:
    current_group = []

    for rucksack in raw_rucksacks.split("\n"):
        current_group.append(rucksack)
        if len(current_group) == 3:
            yield current_group
            current_group = []


def solve_part2(raw_rucksacks: str) -> int:
    sum_of_priorities = 0

    for rucksack_group in rucksack_groups(raw_rucksacks):
        a, b, c = map(set, rucksack_group)
        badge_item = (a & b & c).pop()
        sum_of_priorities += get_priority(badge_item)

    return sum_of_priorities


if __name__ == "__main__":
    solution_part1 = solve_part1(real_input)
    print(f"{solution_part1 = }")
    solution_part2 = solve_part2(real_input)
    print(f"{solution_part2 = }")
