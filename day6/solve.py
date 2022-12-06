from collections import deque
from inputs import test_inputs, real_input


class LastN(deque):
    number_of_distinct_characters: int

    def __init__(self, number_of_distinct_characters: int):
        self.number_of_distinct_characters = number_of_distinct_characters

    @property
    def no_duplicates(self) -> bool:
        return len(self) >= self.number_of_distinct_characters and len(set(self)) == self.number_of_distinct_characters

    def append(self, character: str) -> None:
        if len(self) < self.number_of_distinct_characters:
            super().append(character)
        else:
            super().popleft()
            super().append(character)


def solve(datastream: str, last_n_container: LastN) -> int:
    for index, character in enumerate(datastream):
        last_n_container.append(character)
        if last_n_container.no_duplicates:
            return index + 1


if __name__ == "__main__":
    solution_part1 = solve(real_input, LastN(number_of_distinct_characters=4))
    print(f"{solution_part1 = }")
    solution_part2 = solve(real_input, LastN(number_of_distinct_characters=14))
    print(f"{solution_part2 = }")
