from typing import Generator
from inputs import test_input, real_input


class Assignment:
    start: int
    stop: int

    def __str__(self) -> str:
        return f"{self.start}->{self.stop}"

    def __init__(self, raw_assignment: str) -> None:
        self.start, self.stop = map(int, raw_assignment.split("-"))

    def __contains__(self, other: "Assignment") -> bool:
        return self.start <= other.start and other.stop <= self.stop

    def overlaps_with(self, other: "Assignment") -> bool:
        return self.start <= other.stop and other.start <= self.stop


def assignments(raw_assignments: str) -> Generator[tuple[Assignment, Assignment], None, None]:
    for raw_assignment_pair in raw_assignments.split("\n"):
        a, b = map(Assignment, raw_assignment_pair.split(","))
        yield a, b


def solve(raw_assignments: str) -> tuple[int, int]:
    number_of_fully_contained_assignments = 0
    number_of_assignments_overlapping = 0

    for a, b in assignments(raw_assignments):
        if (a in b) or (b in a):
            number_of_fully_contained_assignments += 1
        if a.overlaps_with(b):
            number_of_assignments_overlapping += 1

    return number_of_fully_contained_assignments, number_of_assignments_overlapping


if __name__ == "__main__":
    result_part1, result_part2 = solve(real_input)
    print(f"{result_part1 = }")
    print(f"{result_part2 = }")
