"""Advent of Code 2020, Day 11: {TITLE_HERE}."""

import logging
import pprint
import math
import itertools, functools
from typing import Counter

import attr, click
import functional
import pandas as pd, numpy as np

import advent.inputs as inputs


AOC_DAY = 11

SIT_CHARS = {"#": True, "L": False}
REVERSE = {None: ".", True: "#", False: "L"}


def parse_floor_plan(input):
    return (
        functional.seq(input.splitlines())
        .map(lambda l: [SIT_CHARS.get(s) for s in list(l)])
        .list()
    )


def write_floor_plan(floor_plan):
    return "\n".join(map(lambda r: "".join(REVERSE.get(c) for c in r), floor_plan))


def step(floor_plan, i, j):
    top_border, bottom_border = i == 0, i == len(floor_plan) - 1
    left_border, right_border = j == 0, j == len(floor_plan[i]) - 1

    neighbors = 0
    if not top_border:
        # NW
        if not left_border and floor_plan[i - 1][j - 1] is True:
            neighbors += 1
        # N
        if floor_plan[i - 1][j] is True:
            neighbors += 1
        # NE
        if not right_border and floor_plan[i - 1][j + 1] is True:
            neighbors += 1

    # W
    if not left_border and floor_plan[i][j - 1] is True:
        neighbors += 1
    # E
    if not right_border and floor_plan[i][j + 1] is True:
        neighbors += 1

    if not bottom_border:
        # SW
        if not left_border and floor_plan[i + 1][j - 1] is True:
            neighbors += 1
        # S
        if floor_plan[i + 1][j] is True:
            neighbors += 1
        # SE
        if not right_border and floor_plan[i + 1][j + 1] is True:
            neighbors += 1

    if floor_plan[i][j] is False:
        return neighbors == 0
    return neighbors < 4


def do_par1(input):
    floor_plan = parse_floor_plan(input)
    previous = ""
    current = write_floor_plan(floor_plan)
    while previous != current:
        floor_plan = [
            [
                None if place is None else step(floor_plan, i, j)
                for j, place in enumerate(row)
            ]
            for i, row in enumerate(floor_plan)
        ]
        previous, current = current, write_floor_plan(floor_plan)

    return Counter(current)["#"]


EXAMPLE = """L.LL.LL.LL
LLLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLLL
L.LLLLLL.L
L.LLLLL.LL"""


def part1():
    """Solution for part 1 of day 11."""
    logging.info("SOLVING DAY 11 PART 1")

    example_1 = do_par1(EXAMPLE)
    click.echo(click.style("EXAMPLE 1 >> ", fg="green") + pprint.pformat(example_1))
    assert example_1 == 37

    result = do_par1("\n".join(inputs.lines_of_day(AOC_DAY)))

    click.echo(click.style("RESULT >> ", fg="green") + pprint.pformat(result))
    # assert result == XXXX  # Valid result for my input


def line(floor_plan, i, j, dir):
    top_border, bottom_border = 0, len(floor_plan)
    left_border, right_border = 0, len(floor_plan[i])

    if "N" in dir:
        i_axis = range(i - 1, top_border - 1, -1)
    elif "S" in dir:
        i_axis = range(i + 1, bottom_border)
    else:
        i_axis = itertools.repeat(i)

    if "W" in dir:
        j_axis = range(j - 1, left_border - 1, -1)
    elif "E" in dir:
        j_axis = range(j + 1, right_border)
    else:
        j_axis = itertools.repeat(j)

    if type(i_axis) == type(itertools.repeat(None)) and type(i_axis) == type(j_axis):
        raise ValueError

    return zip(i_axis, j_axis)


def step2(floor_plan, i, j):
    top_border, bottom_border = i == 0, i == len(floor_plan) - 1
    left_border, right_border = j == 0, j == len(floor_plan[i]) - 1

    def seats_in_view(dir):
        yield from (
            floor_plan[x][y]
            for x, y in line(floor_plan, i, j, dir)
            if floor_plan[x][y] is not None
        )
        yield None

    neighbors = 0
    if not top_border:
        # NW
        if next(seats_in_view("NW")) is True:
            neighbors += 1
        # N
        if next(seats_in_view("N")) is True:
            neighbors += 1
        # NE
        if next(seats_in_view("NE")) is True:
            neighbors += 1

    # W
    if next(seats_in_view("W")) is True:
        neighbors += 1
    # E
    if next(seats_in_view("E")) is True:
        neighbors += 1

    if not bottom_border:
        # SW
        if next(seats_in_view("SW")) is True:
            neighbors += 1
        # N
        if next(seats_in_view("S")) is True:
            neighbors += 1
        # NE
        if next(seats_in_view("SE")) is True:
            neighbors += 1

    if floor_plan[i][j] is False:
        return neighbors == 0
    return neighbors < 5


def do_par2(input):
    floor_plan = parse_floor_plan(input)
    previous = ""
    current = write_floor_plan(floor_plan)
    print(current)
    while previous != current:
        floor_plan = [
            [
                None if place is None else step2(floor_plan, i, j)
                for j, place in enumerate(row)
            ]
            for i, row in enumerate(floor_plan)
        ]
        previous, current = current, write_floor_plan(floor_plan)
        print("=" * 20)
        print(current)

    return Counter(current)["#"]


def part2():
    """Solution for part 2 of day 11."""
    logging.info("SOLVING DAY 11 PART 2")

    example_1 = do_par2(EXAMPLE)
    click.echo(click.style("EXAMPLE 1 >> ", fg="green") + pprint.pformat(example_1))
    assert example_1 == 26

    result = do_par2("\n".join(inputs.lines_of_day(AOC_DAY)))

    click.echo(click.style("RESULT >> ", fg="green") + pprint.pformat(result))
    # assert result == XXXX  # Valid result for my input
