from collections import deque
import pytest
from solve import (
    MonkeyTestDivisible,
    parse_test,
    parse_operation,
    parse_starting_items,
    OperationAdd,
    OperationMultiply,
    OperationSquare,
)


@pytest.mark.parametrize(
    "raw,expected_class,expected_value",
    [
        ["  Operation: new = old * 19", OperationMultiply, 19],
        ["  Operation: new = old + 4", OperationAdd, 4],
        ["  Operation: new = old + 0\n", OperationAdd, 0],
        ["  Operation: new = old * 9\n", OperationMultiply, 9],
        ["  Operation: new = old * old\n", OperationSquare, None],
    ],
)
def test_parse_operation(raw, expected_class, expected_value):
    operation = parse_operation(raw)
    assert isinstance(operation, expected_class)
    if isinstance(expected_class, (OperationAdd, OperationMultiply)):
        assert operation.value == expected_value


@pytest.mark.parametrize(
    "raw,expected_items",
    [
        ["  Starting items: 79, 98", [79, 98]],
        ["  Starting items: ", []],
        ["  Starting items: 12\n", [12]],
        ["Starting items: 120, 98,12, 40\n", [120, 98, 12, 40]],
    ],
)
def test_parse_starting_items(raw, expected_items):
    items = parse_starting_items(raw)
    assert items == deque(expected_items)


@pytest.mark.parametrize(
    "raw,expected_class,expected_value,expected_if_true,expected_if_false",
    [
        [
            "  Test: divisible by 23\n    If true: throw to monkey 0\n    If false: throw to monkey 1",
            MonkeyTestDivisible,
            23,
            0,
            1,
        ],
        [
            "Test: divisible by -1\n    If true: throw to monkey 4\n    If false: throw to monkey 23 ",
            MonkeyTestDivisible,
            -1,
            4,
            23,
        ],
        [
            " Test: divisible by 42\n    If true: throw to monkey 123\n    If false: throw to monkey 8 ",
            MonkeyTestDivisible,
            42,
            123,
            8,
        ],
    ],
)
def test_parse_monkey_test(raw, expected_class, expected_value, expected_if_true, expected_if_false):
    monkey_test = parse_test(raw)
    assert isinstance(monkey_test, expected_class)
    assert monkey_test.value == expected_value
    assert monkey_test.if_true == expected_if_true
    assert monkey_test.if_false == expected_if_false


def test_parse_monkey_test_does_not_parse_0():
    with pytest.raises(ValueError):
        parse_test("Test: divisible by 0")
