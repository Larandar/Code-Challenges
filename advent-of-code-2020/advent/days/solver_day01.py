"""Advent of Code 2020, Day 1: {TITLE_HERE}."""

from functional.pipeline import Sequence

from advent.solver import AdventSolver


def match_reports(values, count):
    """Report matching sum of expenses reports."""
    if count <= 0:
        raise ValueError
    if count == 1:
        yield from (([i], [v], v, v) for i, v in enumerate(values))
        return
    for i, v in enumerate(values):
        yield from (
            ([i, *idx], [v, *vals], s + v, p * v)
            for idx, vals, s, p in match_reports(values[i:], count - 1)
        )


SAMPLE_01 = (1721, 979, 366, 299, 675, 1456)


class Day01Part1_Solver(metaclass=AdventSolver):
    """Solver for part 1/2 of day 1."""

    SAMPLE_RESULTS = {SAMPLE_01: 514579}
    EXPECTED_RESULT = 145875

    def solve(self, puzzle_input: Sequence):
        """Solve part 1/2 of day 1."""
        matching_reports = (
            (vals, p)
            for _, vals, s, p in match_reports(puzzle_input.map(int).list(), 2)
            if s == 2020
        )
        return next(matching_reports)[1]


class Day01Part2_Solver(metaclass=AdventSolver):
    """Solver for part 2/2 of day 1."""

    SAMPLE_RESULTS = {SAMPLE_01: 241861950}
    EXPECTED_RESULT = 69596112

    def solve(self, puzzle_input: Sequence):
        """Solve part 2/2 of day 1."""
        matching_reports = (
            (vals, p)
            for _, vals, s, p in match_reports(puzzle_input.map(int).list(), 3)
            if s == 2020
        )
        return next(matching_reports)[1]
