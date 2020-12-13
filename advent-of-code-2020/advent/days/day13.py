"""Advent of Code 2020, Day 13: {TITLE_HERE}."""

import logging
import pprint
import math
import itertools, functools

import attr, click
import pandas as pd, numpy as np
from functional import seq
import advent.inputs as inputs

from sympy.ntheory.modular import *

AOC_DAY = 13
INPUT_FILE = inputs.file_of_day(AOC_DAY)


def do_part1(lines):
    timestamp, buses = lines
    timestamp = int(timestamp)
    buses = (
        seq(buses.split(","))
        .filter_not(lambda x: x == "x")
        .map(int)
        .sorted(lambda b: timestamp % b)
        .cache()
    )
    next_bus = buses.last()
    return next_bus * (next_bus - (timestamp % next_bus))


def part1():
    """Solution for part 1 of day 13."""
    logging.info("SOLVING DAY 13 PART 1")

    assert do_part1(["939", "7,13,x,x,59,x,31,19"]) == 295
    result = do_part1(inputs.lines_of_day(AOC_DAY))

    click.echo(click.style("RESULT >> ", fg="green") + pprint.pformat(result))
    # assert result == XXXX  # Valid result for my input


def do_part2(lines):
    _, buses = lines

    def schedule(bus, condition):
        t = 0
        while True:
            if condition(t):
                yield t
            t += bus

    def on_schedule(bus, delta):
        def on_schedule_inner(t, debug=False):
            if debug:
                print((t, bus, delta), (t + delta) % bus)
            return (t + delta) % bus == 0

        return on_schedule_inner

    buses = (
        seq(buses.split(","))
        .enumerate()
        .filter_not(lambda x: x[1] == "x")
        .map(lambda x: (x[0], int(x[1])))
        .cache()
    )

    buses_ids = buses.map(lambda x: x[1]).cache()
    delta = buses_ids.first()

    # t = 0
    # conditions = buses.map(lambda x: on_schedule(x[1], x[0])).list()
    # while any(not s(t) for s in conditions):
    #     t += delta

    congruences = buses.map(lambda x: (x[0] % x[1], x[1])).list()
    a, b = solve_congruence(*congruences, check=True)
    return b - a


def part2():
    """Solution for part 2 of day 13."""
    logging.info("SOLVING DAY 13 PART 2")

    sample_01 = do_part2(["x", "7,13,x,x,59,x,31,19"])
    click.echo(click.style("SAMPLE 01 >> ", fg="green") + pprint.pformat(sample_01))
    assert sample_01 == 1068781

    sample_02 = do_part2(["x", "17,x,13,19"])
    click.echo(click.style("SAMPLE 02 >> ", fg="green") + pprint.pformat(sample_02))
    assert sample_02 == 3417

    sample_03 = do_part2(["x", "67,7,59,61"])
    click.echo(click.style("SAMPLE 03 >> ", fg="green") + pprint.pformat(sample_03))
    assert sample_03 == 754018

    result = do_part2(inputs.lines_of_day(AOC_DAY))

    click.echo(click.style("RESULT >> ", fg="green") + pprint.pformat(result))
    # assert result == XXXX  # Valid result for my input
