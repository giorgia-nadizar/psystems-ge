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


def unary_addition(n, p):
    ruleset = []
    content = []
    objects = {"a", "b", "c"}
    r = Rule(["a"], [["c"]], "k", RuleType.SEND_OUT)
    ruleset.append(r)
    r = Rule(["b"], [["c"]], "k", RuleType.SEND_OUT)
    ruleset.append(r)
    for i in range(0, p):
        content.append("a")
    for i in range(p, n):
        content.append("b")
    h = Membrane("h", "")
    k = Membrane("k", content, parent=h)
    h.children = [k]
    return h, ruleset, objects


def unary_multiplication(n, p):
    ruleset = []
    content = []
    objects = {"a", "b"}
    rhs = ["b"] * n
    r = Rule(["a"], [rhs], "k", RuleType.SEND_OUT)
    ruleset.append(r)
    for i in range(0, p):
        content.append("a")
    h = Membrane("h", "")
    k = Membrane("k", content, parent=h)
    h.children = [k]
    return h, ruleset, objects


def unary_div(n, p):
    ruleset = []
    content = []
    objects = {"a", "b"}
    lhs = ["a"] * n
    r = Rule(lhs, [["b"]], "k", RuleType.SEND_OUT)
    ruleset.append(r)
    for i in range(0, p):
        content.append("a")

    h = Membrane("h", "")
    k = Membrane("k", content, parent=h)
    h.children = [k]
    return h, ruleset, objects


def operations(n, p):
    h_add, ruleset_add, objects_add = unary_addition(n, p)
    h_mul, ruleset_mul, objects_mul = unary_multiplication(n, p)
    h_div, ruleset_div, objects_div = unary_div(n, p)

    ruleset = ruleset_mul + ruleset_div + ruleset_add
    objects = objects_mul | objects_div | objects_add

    content = []
    x = random.randint(0, n * n)
    for i in range(0, x):
        content.append("a")
    for i in range(0, x):
        content.append("a")
    for i in range(x, n):
        content.append("b")
    h = Membrane("h", "")
    k = Membrane("k", content, parent=h)
    h.children = [k]

    return h, ruleset, objects


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


def generate_dataset_and_grammar(n, name, p=None, seed=0, setting="standard"):
    if p is None:
        p = n / 2
    random.seed(seed)
    if name == "evolution":
        m, r, obj_all = variable_assignment(n)
    elif name == "send_in":
        m, r, obj_all = send_in(n)
    elif name == "send_out":
        m, r, obj_all = send_out(n)
    elif name == "tm_simulation":
        m, r, obj_all = tm_simulation(n)
    elif name == "unary-add":
        m, r, obj_all = unary_addition(n, p)
    elif name == "unary-mult":
        m, r, obj_all = unary_multiplication(n, p)
    elif name == "unary-div":
        m, r, obj_all = unary_div(n, p)
    elif name == "operations":
        m, r, obj_all = operations(n, p)
    else:
        raise KeyError(f"No dataset for {name}")
    if name != "tm_simulation":
        train = make_train_set(m, r, n)
        labels = ["h", "k"]
    else:
        train = make_train_set(m, r, n ** 2)
        labels = ["h"]
    # save dataset to file
    with bz2.BZ2File(path.join("..", "datasets", f"Psystems/train_{name}_{seed}.pbz2"), 'w') as dataset_file:
        _pickle.dump(train, dataset_file)
    # create grammar file
    if setting == "standard":
        with open(path.join("..", "grammars", "psystems/ruleset.bnf")) as template_grammar_file:
            template_grammar = template_grammar_file.read()
            grammar = template_grammar.replace('LABELS', ' | '.join(labels)).replace('OBJECTS', ' | '.join(obj_all))
            with open(path.join("..", "grammars", f"psystems/ruleset_{name}_{seed}.bnf"), "w+") as target_grammar_file:
                target_grammar_file.write(grammar)
    elif setting == "easy":
        with open(path.join("..", "grammars", f"psystems/ruleset_{name}.bnf")) as template_grammar_file:
            template_grammar = template_grammar_file.read()
            grammar = template_grammar.replace('LABELS', ' | '.join(labels)).replace('OBJECTS', ' | '.join(obj_all))
            with open(path.join("..", "grammars", f"psystems/ruleset_{name}_{seed}.bnf"), "w+") as target_grammar_file:
                target_grammar_file.write(grammar)
    else:
        raise KeyError
    return f"{name}_{seed}"


def mane():
    """ Run program """
    cmd_args, _ = parse_cmd_args(sys.argv[1:])
    generate_dataset_and_grammar(
        n=cmd_args['RULESET_SIZE'],
        name=cmd_args['RULE_TYPE'],
        p=cmd_args['P'],
        seed=cmd_args['DATASET_SEED'],
        setting=cmd_args['SETTING']
    )
    set_params(sys.argv[1:])

    # Run evolution
    individuals = params['SEARCH_LOOP']()

    # Print final review
    get_stats(individuals, end=True)


if __name__ == "__main__":
    mane()
