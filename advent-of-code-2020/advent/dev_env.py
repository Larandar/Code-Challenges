"""Commands for handling dev environment."""
import click

from advent.const import DAYS_DIR

COMMON_IMPORTS = """
from functional.pipeline import Sequence

from advent.solver import AdventSolver
"""

PART_FUNCTION = '''
class Day{day:02d}Part{part}_Solver(metaclass=AdventSolver):
    """Solver for part {part}/2 of day {day}."""

    SAMPLE_RESULTS = {{}}
    EXPECTED_RESULT = None

    def solve(self, puzzle_input: Sequence):
        """Solve part {part}/2 of day {day}."""
        raise NotImplementedError("Solution not yet implemented")
'''


@click.command()
@click.argument("day", type=int)
def create(day):
    """Command to create an environment for the next day."""
    py_file = DAYS_DIR / f"solver_day{day:02d}.py"
    if py_file.exists():
        raise ValueError(f"File {py_file} already exists.")

    with py_file.open("w") as f:
        f.write(
            "\n".join(
                [
                    f'"""Advent of Code 2020, Day {day}: {{TITLE_HERE}}."""',
                    COMMON_IMPORTS,
                    PART_FUNCTION.format(day=day, part=1),
                    PART_FUNCTION.format(day=day, part=2),
                ]
            )
        )


if __name__ == "__main__":
    create()
