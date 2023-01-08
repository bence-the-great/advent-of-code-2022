import pytest
from solve import Position


@pytest.mark.parametrize(
    "head,tail,expected_tail,expected_visited_positions",
    [
        # Cases, where the tail should not move
        [Position(x=0, y=0), Position(x=0, y=0), Position(x=0, y=0), [Position(x=0, y=0)]],
        [Position(x=1, y=0), Position(x=0, y=0), Position(x=0, y=0), [Position(x=0, y=0)]],
        [Position(x=0, y=1), Position(x=0, y=0), Position(x=0, y=0), [Position(x=0, y=0)]],
        [Position(x=1, y=1), Position(x=0, y=0), Position(x=0, y=0), [Position(x=0, y=0)]],
        [Position(x=4, y=5), Position(x=4, y=4), Position(x=4, y=4), [Position(x=4, y=4)]],
        [Position(x=5, y=41), Position(x=4, y=41), Position(x=4, y=41), [Position(x=4, y=41)]],
        [Position(x=321, y=20), Position(x=322, y=21), Position(x=322, y=21), [Position(x=322, y=21)]],
    ],
)
def test_tail_follow_algorithm_should_not_move(
    head: Position,
    tail: Position,
    expected_tail: Position,
    expected_visited_positions: list[Position],
):
    visited_positions = list(tail.follow(head))

    assert tail == expected_tail
    assert visited_positions == expected_visited_positions


@pytest.mark.parametrize(
    "head,tail,expected_tail,expected_visited_positions",
    [
        [Position(x=2, y=0), Position(x=0, y=0), Position(x=1, y=0), [Position(x=0, y=0), Position(x=1, y=0)]],
        [Position(x=6, y=2), Position(x=6, y=4), Position(x=6, y=3), [Position(x=6, y=4), Position(x=6, y=3)]],
        [
            Position(x=2, y=5),
            Position(x=2, y=2),
            Position(x=2, y=4),
            [Position(x=2, y=2), Position(x=2, y=3), Position(x=2, y=4)],
        ],
        [
            Position(x=23, y=9),
            Position(x=27, y=9),
            Position(x=24, y=9),
            [Position(x=27, y=9), Position(x=26, y=9), Position(x=25, y=9), Position(x=24, y=9)],
        ],
    ],
)
def test_tail_follow_algorithm_should_move(
    head: Position,
    tail: Position,
    expected_tail: Position,
    expected_visited_positions: list[Position],
):
    visited_positions = list(tail.follow(head))

    assert tail == expected_tail
    assert visited_positions == expected_visited_positions


@pytest.mark.parametrize(
    "head,tail,expected_tail,expected_visited_positions",
    [
        [Position(x=2, y=1), Position(x=0, y=0), Position(x=1, y=1), [Position(x=0, y=0), Position(x=1, y=1)]],
        [Position(x=2, y=2), Position(x=0, y=0), Position(x=1, y=1), [Position(x=0, y=0), Position(x=1, y=1)]],
        [Position(x=0, y=0), Position(x=2, y=2), Position(x=1, y=1), [Position(x=2, y=2), Position(x=1, y=1)]],
        [Position(x=6, y=-4), Position(x=4, y=-2), Position(x=5, y=-3), [Position(x=4, y=-2), Position(x=5, y=-3)]],
        [
            Position(x=0, y=0),
            Position(x=-1, y=3),
            Position(x=0, y=1),
            [Position(x=-1, y=3), Position(x=0, y=2), Position(x=0, y=1)],
        ],
        [
            Position(x=10, y=8),
            Position(x=11, y=5),
            Position(x=10, y=7),
            [Position(x=11, y=5), Position(x=10, y=6), Position(x=10, y=7)],
        ],
        [Position(x=12, y=4), Position(x=13, y=6), Position(x=12, y=5), [Position(x=13, y=6), Position(x=12, y=5)]],
    ],
)
def test_tail_follow_algorithm_should_move_diagonally(
    head: Position,
    tail: Position,
    expected_tail: Position,
    expected_visited_positions: list[Position],
):
    visited_positions = list(tail.follow(head))

    assert tail == expected_tail
    assert visited_positions == expected_visited_positions
