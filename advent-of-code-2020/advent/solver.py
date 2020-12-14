"""A metaclass for making pytest integrated solver."""
import click
import pytest
from functional import seq
from functional.pipeline import Sequence

import advent.inputs as inputs


def report(color=None, **items):
    """Report KPI in a pretty way."""
    for item, value in items.items():
        if color is not None:
            item = click.style(f"{item.upper()} >>>", fg=color)
        else:
            item = f"{item.upper()} >>>"
        click.echo(f"{item} {value}")


def make_solve_method(puzzle_input, expected):
    """Make a solve method for py.test to execute."""

    def inner_test(self):
        parsed_input = self.parse_input(puzzle_input)
        result = self.solve(parsed_input)
        report(result=result, color="green")
        assert result == expected

    if expected is None:
        # By marking test as expecting failure, we can ignore part2 until we start it
        # For that the solve method must raise a NotImplementedError
        inner_test = pytest.mark.xfail(raises=NotImplementedError)(inner_test)

    return inner_test


class AdventSolver(type):
    """A metaclass for making pytest integrated solver."""

    def __new__(cls, name, bases, dct):
        """Create a new class with dynamicly added solve_for methods."""
        day, part = int(name[3:5]), int(name[9])

        # Adding a default parse_input function that just convert to a Sequence
        # Overwriting methods should expect an a Sequence or a Tuple
        if "parse_input" not in dct:
            dct["parse_input"] = (
                lambda _, puzzle_input: puzzle_input
                if isinstance(puzzle_input, Sequence)
                else seq(puzzle_input)
            )

        for i, (sample, expected) in enumerate(dct.pop("SAMPLE_RESULTS", {}).items()):
            sample_name = f"sample_{i+1:02d}"
            solve_for = make_solve_method(sample, expected)
            solve_for.__name__ = f"solve_for_{sample_name}"
            solve_for.__doc__ = f"Solve for {sample_name.replace('_', ' ')}."
            dct[solve_for.__name__] = solve_for

        expected_result = dct.pop("EXPECTED_RESULT", None)
        solve_for = make_solve_method(inputs.lines_of_day(day), expected_result)
        solve_for.__name__ = "solve_for_input_of_day"
        solve_for.__doc__ = f"Solve for input of day {day} part {part}/2."
        dct[solve_for.__name__] = solve_for

        return super().__new__(cls, name, bases, dct)
