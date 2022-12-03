import sys
import inputs
from typing import Generator, Iterable


def line_reader(input: str) -> Generator[str, None, None]:
    for line in input.split("\n"):
        yield line


def count_calories(lines: Iterable[str]) -> int:
    calorie_count = 0

    for line in lines:
        if line == "":
            break
        calorie_count += int(line)
    else:
        raise StopIteration

    return calorie_count


def collect_calories(input: str) -> list[int]:
    elf_calories = []
    lines = line_reader(input)

    while True:
        try:
            calories = count_calories(lines)
        except StopIteration:
            break
        finally:
            elf_calories.append(calories)

    return elf_calories


if __name__ == "__main__":
    elf_calories = collect_calories(getattr(inputs, sys.argv[1]))
    print(f"max: {max(elf_calories)}")
    print(f"top3: {sum(sorted(elf_calories)[-3:])}")
