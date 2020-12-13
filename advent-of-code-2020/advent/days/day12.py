"""Advent of Code 2020, Day 12: {TITLE_HERE}."""

import logging
import pprint
import math
import itertools, functools

import attr, click
import pandas as pd, numpy as np
from functional import seq
import advent.inputs as inputs


AOC_DAY = 12
INPUT_FILE = inputs.file_of_day(AOC_DAY)

DIR_MAP = {"E": (0, 1), "N": (1, 0), "W": (0, -1), "S": (-1, 0)}
DIR_NEXT = {"N": "E", "E": "S", "S": "W", "W": "N"}
DIR_PREV = {"N": "W", "E": "N", "S": "E", "W": "S"}


def move_ship(pos, order):
    d, (x, y) = pos
    dir, v = order

    if dir in DIR_MAP:
        pass
    elif dir == "R":
        for _ in range(v // 90):
            d = DIR_NEXT[d]
        print(pos, order, (d, (x, y)))
        return (d, (x, y))
    elif dir == "L":
        for _ in range(v // 90):
            d = DIR_PREV[d]
        print(pos, order, (d, (x, y)))
        return (d, (x, y))
    elif dir == "F":
        dir = d
    else:
        raise ValueError(f"Invalid dir {dir}")
    vx, vy = DIR_MAP[dir]
    coord = (x + v * vx, y + v * vy)

    print(pos, order, (d, coord))
    return (d, coord)


def do_part1(lines):

    final_pos = (
        seq(lines)
        .map(lambda x: (x[0], int(x[1:])))
        .reduce(
            move_ship,
            ("E", (0, 0)),
        )[1]
    )

    return sum(map(abs, final_pos))


SAMPLE_01 = """
F10
N3
F7
R90
F11
""".strip()


def part1():
    """Solution for part 1 of day 12."""
    logging.info("SOLVING DAY 12 PART 1")

    sample_01 = do_part1(SAMPLE_01.splitlines(False))
    click.echo(click.style("SAMPLE 01 >> ", fg="green") + pprint.pformat(sample_01))
    assert sample_01 == 25

    result = do_part1(inputs.lines_of_day(AOC_DAY))

    click.echo(click.style("RESULT >> ", fg="green") + pprint.pformat(result))
    assert result == 757  # Valid result for my input


def move_ship2(state, order):
    waypoint, coord = state
    (wx, wy), (x, y) = state
    dir, v = order

    # Move waypoint
    if dir in DIR_MAP:
        vx, vy = DIR_MAP[dir]
        waypoint = (
            wx + vx * v,
            wy + vy * v,
        )
        print(state, order, (waypoint, coord))
        return (waypoint, coord)

    # Rotate waypoint
    elif dir in "LR":
        degrees = v if dir == "R" else -v
        radians = -(math.pi * degrees / 180)

        c, s = np.cos(radians), np.sin(radians)

        j = np.matrix([[c, s], [-s, c]])
        m = np.dot(j, [wx, wy])

        waypoint = (float(m.T[0]), float(m.T[1]))
        print(state, order, (waypoint, coord))
        return (waypoint, coord)

    # Forward to waypoint
    elif dir == "F":
        coord = (x + wx * v, y + wy * v)
        print(state, order, (waypoint, coord))
        return (waypoint, coord)
    else:
        raise ValueError(f"Invalid dir {dir}")


def do_part2(lines):

    final_pos = (
        seq(lines)
        .map(lambda x: (x[0], int(x[1:])))
        .reduce(
            move_ship2,
            ((1, 10), (0, 0)),
        )[1]
    )

    return sum(map(abs, final_pos))


def part2():
    """Solution for part 2 of day 12."""
    logging.info("SOLVING DAY 12 PART 2")

    sample_01 = do_part2(SAMPLE_01.splitlines(False))
    click.echo(click.style("SAMPLE 01 >> ", fg="green") + pprint.pformat(sample_01))
    assert sample_01 == 286

    result = do_part2(inputs.lines_of_day(AOC_DAY))

    click.echo(click.style("RESULT >> ", fg="green") + pprint.pformat(result))
    assert (
        math.floor(result) == 51249 or math.ceil(result) == 51249
    )  # Valid result for my input
