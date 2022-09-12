from Membrane import Membrane, Rule, RuleType
from RuleEvo import RuleEvo, evolution_strategy, detailed_errors
import sys
import json
import os


def make_train_set(membrane, ruleset, steps):
    data = []
    for i in range(0, steps):
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
            r = Rule([f"x({i},{j+1})"], [[f"x({i},{j})"]], "k",
                     RuleType.EVOLUTION)
            ruleset.append(r)
            objects.add(f"x({i},{j+1})")
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
    for i in range(0, n-1):
        #  δ(q,1) = (q,0,→)
        r = Rule([f"q({i})", f"1_{i}"],
                 [[f"q({i+1})", f"0_{i}"]], "h",
                 RuleType.EVOLUTION)
        ruleset.append(r)
        objects.add(f"q({i})")
        objects.add(f"q({i+1})")
    for i in range(1, n):
        # δ(q,0) = (r,1,←)
        r = Rule([f"q({i})", f"0_{i}"],
                 [[f"r({i-1})", f"1_{i}"]], "h",
                 RuleType.EVOLUTION)
        ruleset.append(r)
        objects.add(f"r({i-1})")
        objects.add(f"({i})")
    for i in range(1, n):
        # δ(r,0) = (r,0,←) and δ(r,1) = (r,1,←)
        r = Rule([f"r({i})", f"0_{i}"],
                 [[f"r({i-1})", f"0_{i}"]], "h",
                 RuleType.EVOLUTION)
        ruleset.append(r)
        objects.add(f"r({i})")
        objects.add(f"({i-1})")
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
            r = Rule([f"x({i},{j})"], [[f"x({i},{j-1})"]], "h",
                     RuleType.EVOLUTION)
            ruleset.append(r)
            objects.add(f"x({i},{j})")
            objects.add(f"x({i},{j-1})")
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
            r = Rule([f"x({i},{j})"], [[f"x({i},{j-1})"]], "k",
                     RuleType.EVOLUTION)
            ruleset.append(r)
            objects.add(f"x({i},{j})")
            objects.add(f"x({i},{j-1})")
        r = Rule([f"x({i},0)"], [[f"x({i})"]], "k", RuleType.SEND_OUT)
        ruleset.append(r)
        content.append(f"x({i},{i})")
        objects.add(f"x({i},0)")
        objects.add(f"x({i})")
    h = Membrane("h", [])
    k = Membrane("k", content, parent=h)
    h.children = [k]
    return h, ruleset, objects



def read_param(filename):
    with open(filename) as f:
        conf = json.load(f)
        max_lhs=conf["max_lhs"]
        max_rhs=conf["max_rhs"]
        max_ruleset_size=conf["max_ruleset_size"]
        max_mutation=conf["max_mutation"]
        mu=conf["mu"]
    return max_lhs, max_rhs, max_ruleset_size, max_mutation, mu




def read_conf(filename, objects, labels, train):
    with open(filename) as f:
        conf = json.load(f)
    evo = RuleEvo(objects,
                  labels,
                  lambda x, y: x.distance(y),
                  train,
                  max_lhs=conf["max_lhs"],
                  max_rhs=conf["max_rhs"],
                  min_ruleset_size=conf["min_ruleset_size"],
                  max_ruleset_size=conf["max_ruleset_size"],
                  max_mutation=conf["max_mutation"],
                  mu=conf["mu"],
                  lmbd=conf["lmbd"],
                  generations=conf["generations"])
    return evo


def experiments(n, name, config):
    if name == "assignment":
        m, r, obj_all = variable_assignment(n)
    elif name == "send-in":
        m, r, obj_all = send_in(n)
    elif name == "send-out":
        m, r, obj_all = send_out(n)
    elif name == "tm":
        m, r, obj_all = tm_simulation(n)
    else:
        raise KeyError(f"No dataset for {name}")
    if name != "tm":
        train = make_train_set(m, r, n)
        evo = read_conf(config, list(obj_all), ["h", "k"], train)
    else:
        train = make_train_set(m, r, n**2)
        evo = read_conf(config, list(obj_all), ["h"], train)
    pop, best_fit = evolution_strategy(evo)
    opt = pop[0]
    for r in opt:
        print(r)
    print("===")
    detailed_errors(evo, opt)
    return opt, best_fit


if __name__ == '__main__':
    try:
        prefix = sys.argv[5]
    except Exception:
        prefix = "out"
    try:
        config = sys.argv[4]
    except Exception:
        config = "conf.json"
    try:
        repetitions = int(sys.argv[3])
    except Exception:
        repetitions = 1
    max_lhs, max_rhs, max_ruleset_size, max_mutation, mu = read_param(config)
    all_opts = []
    all_best = []
    
    if sys.argv[1] != sys.argv[5][:-2]:
        print("not the same model")
        sys.exit()
    
    if sys.argv[2] != sys.argv[5][-1]:
        print("not the same number")
        sys.exit()
    
    for i in range(0, repetitions):
        print("Repetition : " + str(i))
        opt, best_fit = experiments(int(sys.argv[2]), sys.argv[1], config)
        all_opts.append(opt)
        all_best.append(best_fit)
    dir0 = "results/"
    dir1 = dir0 + str(mu) + "/"
    if not os.path.exists(dir1):
        os.mkdir(dir1)
    dir2 = dir1 + str(max_ruleset_size) + "/"
    if not os.path.exists(dir2):
        os.mkdir(dir2)
    dir3 = dir2 + str(max_mutation) + "/"
    if not os.path.exists(dir3):
        os.mkdir(dir3)
    dir4 = dir3 + str(max_lhs) + "/"
    if not os.path.exists(dir4):
        os.mkdir(dir4)
    dir5 = dir4 + str(max_rhs) + "/"
    if not os.path.exists(dir5):
        os.mkdir(dir5)
    with open(f"{dir5 + prefix}-fitness.csv", "w") as csv:
        for gen in range(0, len(all_best[0])):
            for run in range(0, repetitions-1):
                csv.write(f"{all_best[run][gen]}, ")
            csv.write(f"{all_best[repetitions-1][gen]}\n")
    with open(f"{dir5 + prefix}-rules.txt", "w") as f:
        for run in range(0, repetitions):
            for rule in all_opts[run]:
                f.write(f"{rule}\n")
            f.write("===\n")
