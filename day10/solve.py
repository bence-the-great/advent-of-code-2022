from dataclasses import dataclass, field
from typing import Generator
from inputs import test_input, real_input


@dataclass
class Registers:
    reg_x: int = field(init=False, default=1)


@dataclass
class Instruction:
    cycle_count: int = field(init=False, default=1)

    def do_work(self, registers: Registers) -> Registers:
        return registers


@dataclass
class Noop(Instruction):
    pass


@dataclass
class AddX(Instruction):
    cycle_count: int = field(init=False, default=2)
    value: int

    def do_work(self, registers: Registers) -> Registers:
        registers.reg_x += self.value
        return super().do_work(registers)


def parse_instruction(raw_instruction: str) -> Instruction:
    instruction = raw_instruction.split()

    if instruction[0] == "noop":
        return Noop()
    elif instruction[0] == "addx":
        return AddX(value=int(instruction[1]))
    else:
        raise Exception(f"unrecognized instruction: {raw_instruction}")


def instructions(raw_program: str) -> Generator[Instruction, None, None]:
    for raw_instruction in raw_program.split("\n"):
        yield parse_instruction(raw_instruction)


def solve(raw_program: str) -> int:
    sum_signal_strength = 0
    cycle_number = 0
    registers = Registers()

    for instruction in instructions(raw_program):
        for _ in range(instruction.cycle_count):
            cycle_number += 1
            if (cycle_number % 40) >= registers.reg_x and (cycle_number % 40) <= (registers.reg_x + 2):
                print("█", end="")
            else:
                print(" ", end="")
            if cycle_number % 40 == 0:
                print()
            if (cycle_number + 20) % 40 == 0:
                sum_signal_strength += cycle_number * registers.reg_x
        instruction.do_work(registers)

    return sum_signal_strength


if __name__ == "__main__":
    sum_signal_strength = solve(real_input)
    print(f"{sum_signal_strength = }")
