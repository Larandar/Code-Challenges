"""Advent of Code 2020, Day 9: {TITLE_HERE}."""
import sys
import logging
import pprint
import math
import itertools, functools

import attr, click
import pandas as pd, numpy as np

import advent.inputs as inputs


AOC_DAY = 9
INPUT_FILE = inputs.file_of_day(AOC_DAY)
sys.setrecursionlimit(15000)


@functools.lru_cache
def how_sum(nb, parts):
    if nb == 0:
        return []
    if nb < 0:
        return None
    for i, o in enumerate(parts):
        sub = how_sum(nb - o, tuple([*parts[:i], *parts[i + 1 :]]))
        if sub is not None:
            return sub + [o]
    return None


def part1():
    """Solution for part 1 of day 9."""
    logging.info("SOLVING DAY 9 PART 1")

    numbers = inputs.records_of_day(AOC_DAY).map(int).list()

    result = None
    for i, x in enumerate(numbers):
        if i < 25:
            continue
        s = how_sum(x, tuple(numbers[i - 25 : i]))
        if s is None:
            result = x
            break

    click.echo(click.style("RESULT >> ", fg="green") + pprint.pformat(result))
    assert result == 27911108  # Valid result for my input


def part2():
    """Solution for part 2 of day 9."""
    logging.info("SOLVING DAY 9 PART 2")

    numbers = inputs.records_of_day(AOC_DAY).map(int).list()

    result = None
    for w in range(2, len(numbers)):
        for i in range(len(numbers)):
            sub_list = numbers[i : i + w]
            if sum(sub_list) == 27911108:
                result = min(sub_list) + max(sub_list)
                break
        if result is not None:
            break

    click.echo(click.style("RESULT >> ", fg="green") + pprint.pformat(result))
    assert result == 4023754  # Valid result for my input
