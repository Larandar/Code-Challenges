"""Advent of Code 2020, Day 10: {TITLE_HERE}."""

from collections import defaultdict
import logging
import pprint
import math
import itertools, functools
from functional import seq
import attr, click
import pandas as pd, numpy as np

import advent.inputs as inputs


AOC_DAY = 10
INPUT_FILE = inputs.file_of_day(AOC_DAY)


@functools.lru_cache
def adapters_chain(adapters, target):
    chain = []
    jolts = 0
    adapters = list(sorted(adapters))
    for a in adapters:
        chain.append((jolts, a, a - jolts))
        jolts = a
    return chain


def part1():
    """Solution for part 1 of day 10."""
    logging.info("SOLVING DAY 10 PART 1")

    in_bag = set()
    adapters = defaultdict(list)
    (
        inputs.records_of_day(AOC_DAY)
        .map(int)
        .for_each(
            lambda x: adapters[x - 3].append(x)
            or adapters[x - 2].append(x)
            or adapters[x - 1].append(x)
            or in_bag.add(x)
        )
    )

    chain = adapters_chain(frozenset(in_bag), max(in_bag) + 3)
    steps = seq(chain).map(lambda x: x[2]).count_by_value()
    pprint.pprint(steps)
    result = "Hello World"

    click.echo(click.style("RESULT >> ", fg="green") + pprint.pformat(result))
    assert result == 2343  # Valid result for my input


@functools.lru_cache
def distinct_ways(adapters, jolts):
    if jolts == 0:
        return 1

    result = 0
    for i, a in enumerate(adapters):
        print(adapters, i, a)
        if a < jolts - 3:
            break

        result += distinct_ways(adapters[i + 1 :], a)

    print(result)
    return result


def part2():
    """Solution for part 2 of day 10."""
    logging.info("SOLVING DAY 10 PART 2")

    assert (
        distinct_ways(
            adapters := (
                tuple(
                    seq(
                        """28
33
18
42
31
14
46
20
48
47
24
23
49
45
19
38
39
11
1
32
25
35
8
17
7
9
4
2
34
10
3""".splitlines()
                    )
                    .map(int)
                    .sorted()
                    .reverse()
                    .list()
                    + [0]
                )
            ),
            max(adapters) + 3,
        )
        == 19208
    )

    adapters = inputs.records_of_day(AOC_DAY).map(int).sorted().reverse().list() + [0]
    result = distinct_ways(tuple(adapters), max(adapters) + 3)

    click.echo(click.style("RESULT >> ", fg="green") + pprint.pformat(result))
    # assert result == XXXX  # Valid result for my input
