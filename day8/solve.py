from inputs import test_input, real_input


def parse_trees(raw_trees: str) -> list[list[int]]:
    lines = []
    for line in raw_trees.split("\n"):
        lines.append(list(map(int, line)))
    return lines


def left(tree_lines: list[list[int]], line_number: int, tree_number: int) -> list[int]:
    return tree_lines[line_number][:tree_number]


def right(tree_lines: list[list[int]], line_number: int, tree_number: int) -> list[int]:
    return tree_lines[line_number][tree_number + 1 :]


def top(tree_lines: list[list[int]], line_number: int, tree_number: int) -> list[int]:
    return [t[tree_number] for t in tree_lines[:line_number]]


def bottom(tree_lines: list[list[int]], line_number: int, tree_number: int) -> list[int]:
    return [t[tree_number] for t in tree_lines[line_number + 1 :]]


def part1(tree_lines: list[list[int]]) -> int:
    visible = 0
    for line_number, line in enumerate(tree_lines):
        for tree_number, tree in enumerate(line):
            if (
                (tree > max(left(tree_lines, line_number, tree_number), default=-1))
                or (tree > max(right(tree_lines, line_number, tree_number), default=-1))
                or (tree > max(top(tree_lines, line_number, tree_number), default=-1))
                or (tree > max(bottom(tree_lines, line_number, tree_number), default=-1))
            ):
                visible += 1
    return visible


def get_scenic_score(tree: int, other_trees: list[int]) -> int:
    scenic_score = 0

    for other_tree in other_trees:
        scenic_score += 1
        if other_tree >= tree:
            break

    return scenic_score


def part2(tree_lines: list[list[int]]) -> int:
    max_scenic_score = 0
    for line_number, line in enumerate(tree_lines):
        for tree_number, tree in enumerate(line):
            scenic_score_left = get_scenic_score(tree, reversed(left(tree_lines, line_number, tree_number)))
            scenic_score_right = get_scenic_score(tree, right(tree_lines, line_number, tree_number))
            scenic_score_top = get_scenic_score(tree, reversed(top(tree_lines, line_number, tree_number)))
            scenic_score_bottom = get_scenic_score(tree, bottom(tree_lines, line_number, tree_number))
            scenic_score = scenic_score_left * scenic_score_right * scenic_score_top * scenic_score_bottom
            max_scenic_score = max(max_scenic_score, scenic_score)
    return max_scenic_score


if __name__ == "__main__":
    trees = parse_trees(real_input)

    visible_trees = part1(trees)
    print(f"{visible_trees = }")

    max_scenic_score = part2(trees)
    print(f"{max_scenic_score = }")
