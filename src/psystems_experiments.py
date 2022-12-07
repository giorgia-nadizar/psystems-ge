#! /usr/bin/env python

# PonyGE2
# Copyright (c) 2017 Michael Fenton, James McDermott,
#                    David Fagan, Stefan Forstenlechner,
#                    and Erik Hemberg
# Hereby licensed under the GNU GPL v3.
""" Python GE implementation """
import _pickle
import bz2
import random
from os import path

from psystems.Membrane import Membrane
from psystems.Rule import Rule, RuleType
from utilities.algorithm.command_line_parser import parse_cmd_args
from utilities.algorithm.general import check_python_version
from stats.stats import get_stats
from algorithm.parameters import params, set_params
import sys

check_python_version()


def make_train_set(membrane, ruleset, steps):
    data = []
    for _ in range(0, steps):
        before = Membrane.clone(membrane)
        membrane.apply(ruleset)
        after = Membrane.clone(membrane)
        data.append((before, after))
    return data


def variable_assignment(n):
    ruleset = []
    content = []
    objects = set()
    for i in range(0, n):
        for j in range(0, i):
            r = Rule([f"x({i},{j + 1})"], [[f"x({i},{j})"]], "k",
                     RuleType.EVOLUTION)
            ruleset.append(r)
            objects.add(f"x({i},{j + 1})")
            objects.add(f"x({i},{j})")
        r = Rule([f"x({i},0)"], [[f"t{i}"], [f"f{i}"]], "k", RuleType.DIVISION)
        ruleset.append(r)
        content.append(f"x({i},{i})")
        objects.add(f"x({i},0)")
        objects.add(f"t{i}")
        objects.add(f"f{i}")
    h = Membrane("h", "")
    k = Membrane("k", content, parent=h)
    h.children = [k]
    return h, ruleset, objects


def tm_simulation(n):
    ruleset = []
    content = []
    objects = set()
    for i in range(0, n - 1):
        #  δ(q,1) = (q,0,→)
        r = Rule([f"q({i})", f"1_{i}"],
                 [[f"q({i + 1})", f"0_{i}"]], "h",
                 RuleType.EVOLUTION)
        ruleset.append(r)
        objects.add(f"q({i})")
        objects.add(f"q({i + 1})")
    for i in range(1, n):
        # δ(q,0) = (r,1,←)
        r = Rule([f"q({i})", f"0_{i}"],
                 [[f"r({i - 1})", f"1_{i}"]], "h",
                 RuleType.EVOLUTION)
        ruleset.append(r)
        objects.add(f"r({i - 1})")
        objects.add(f"({i})")
    for i in range(1, n):
        # δ(r,0) = (r,0,←) and δ(r,1) = (r,1,←)
        r = Rule([f"r({i})", f"0_{i}"],
                 [[f"r({i - 1})", f"0_{i}"]], "h",
                 RuleType.EVOLUTION)
        ruleset.append(r)
        objects.add(f"r({i})")
        objects.add(f"({i - 1})")
    r = Rule(["r(0)"],
             [["q(0)"]], "h",
             RuleType.EVOLUTION)
    ruleset.append(r)
    r = Rule(["q(0)", "0_0"],
             [["q(0)", "1_0"]], "h",
             RuleType.EVOLUTION)
    ruleset.append(r)
    objects.add("r(0)")
    objects.add("q(0)")
    # tape objects
    for i in range(0, n):
        objects.add(f"0_{i})")
        objects.add(f"1_{i})")
    for i in range(0, n):
        content.append(f"0_{i}")
    content.append("q(0)")
    h = Membrane("h", content)
    return h, ruleset, objects


def send_in(n):
    ruleset = []
    content = []
    objects = set()
    for i in range(0, n):
        for j in range(i, 0, -1):
            r = Rule([f"x({i},{j})"], [[f"x({i},{j - 1})"]], "h",
                     RuleType.EVOLUTION)
            ruleset.append(r)
            objects.add(f"x({i},{j})")
            objects.add(f"x({i},{j - 1})")
        r = Rule([f"x({i},0)"], [[f"x({i})"]], "k", RuleType.SEND_IN)
        ruleset.append(r)
        content.append(f"x({i},{i})")
        objects.add(f"x({i},0)")
        objects.add(f"x({i})")
    h = Membrane("h", content)
    k = Membrane("k", [], parent=h)
    h.children = [k]
    return h, ruleset, objects


def send_out(n):
    ruleset = []
    content = []
    objects = set()
    for i in range(0, n):
        for j in range(i, 0, -1):
            r = Rule([f"x({i},{j})"], [[f"x({i},{j - 1})"]], "k",
                     RuleType.EVOLUTION)
            ruleset.append(r)
            objects.add(f"x({i},{j})")
            objects.add(f"x({i},{j - 1})")
        r = Rule([f"x({i},0)"], [[f"x({i})"]], "k", RuleType.SEND_OUT)
        ruleset.append(r)
        content.append(f"x({i},{i})")
        objects.add(f"x({i},0)")
        objects.add(f"x({i})")
    h = Membrane("h", [])
    k = Membrane("k", content, parent=h)
    h.children = [k]
    return h, ruleset, objects


def generate_dataset_and_grammar(n, name, seed=0):
    random.seed(seed)
    if name == "evolution":
        m, r, obj_all = variable_assignment(n)
    elif name == "send_in":
        m, r, obj_all = send_in(n)
    elif name == "send_out":
        m, r, obj_all = send_out(n)
    elif name == "division":
        m, r, obj_all = tm_simulation(n)
    else:
        raise KeyError(f"No dataset for {name}")
    if name != "division":
        train = make_train_set(m, r, n)
        labels = ["h", "k"]
    else:
        train = make_train_set(m, r, n ** 2)
        labels = ["h"]
    # save dataset to file
    with bz2.BZ2File(path.join("..", "datasets", f"Psystems/train_{name}_{seed}.pbz2"), 'w') as dataset_file:
        _pickle.dump(train, dataset_file)
    # create grammar file
    with open(path.join("..", "grammars", "psystems/ruleset.bnf")) as template_grammar_file:
        template_grammar = template_grammar_file.read()
        grammar = template_grammar.replace('LABELS', ' | '.join(labels)).replace('OBJECTS', ' | '.join(obj_all))
        with open(path.join("..", "grammars", f"psystems/ruleset_{name}_{seed}.bnf"), "w+") as target_grammar_file:
            target_grammar_file.write(grammar)
    return f"{name}_{seed}"


def mane():
    """ Run program """
    cmd_args, _ = parse_cmd_args(sys.argv[1:])
    generate_dataset_and_grammar(cmd_args['RULESET_SIZE'], cmd_args['RULE_TYPE'], cmd_args['DATASET_SEED'])
    set_params(sys.argv[1:])

    # Run evolution
    individuals = params['SEARCH_LOOP']()

    # Print final review
    get_stats(individuals, end=True)


if __name__ == "__main__":
    mane()
