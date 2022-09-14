from Membrane import Membrane
from Rule import Rule, RuleType
import random as rnd


class RuleEvo:

    def __init__(self, objects, labels,
                 distance,
                 train_set,
                 test_set=None,
                 max_lhs=1,
                 max_rhs=1,
                 min_ruleset_size=1,
                 max_ruleset_size=10,
                 max_mutation=10,
                 mu=1,
                 lmbd=10,
                 generations=1000):
        self.objects = objects
        self.labels = labels
        self.distance = distance
        self.train_set = train_set
        self.test_set = test_set
        self.max_lhs = max_lhs
        self.max_rhs = max_rhs
        self.min_ruleset_size = min_ruleset_size
        self.max_ruleset_size = max_ruleset_size
        self.max_mutation = max_mutation
        self.mu = mu
        self.lmbd = lmbd
        self.generations = generations


def random_ruleset(evo):
    n = rnd.randint(evo.min_ruleset_size, evo.max_ruleset_size)
    return [random_rule(evo) for i in range(0, n)]


def random_rule(evo):
    lhs_len = rnd.randint(1, evo.max_lhs)
    rhs_len = rnd.randint(1, evo.max_rhs)
    lhs = rnd.choices(evo.objects, k=lhs_len)
    rhs = [rnd.choices(evo.objects, k=rhs_len)]
    label = rnd.choice(evo.labels)
    rule_type = rnd.choice([r for r in RuleType])
    if rule_type == RuleType.DIVISION:
        rhs2_len = rnd.randint(1, evo.max_rhs)
        rhs.append(rnd.choices(evo.objects, k=rhs2_len))
    return Rule(lhs, rhs, label, rule_type)


def mutation(evo, ruleset):
    w = list(range(evo.max_mutation, 0, -1))
    repetitions = rnd.choices(range(1, evo.max_mutation + 1), weights=w, k=1)
    mutated = ruleset[:]
    for i in range(0, repetitions[0]):
        can_remove = False
        can_add = False
        if len(mutated) > evo.min_ruleset_size:
            can_remove = True
        if len(mutated) < evo.max_ruleset_size:
            can_add = True
        if can_remove and (not can_add or rnd.choice([True, False])):
            r = rnd.choice(mutated)
            mutated.remove(r)
        else:
            r = random_rule(evo)
            mutated = [r] + mutated
    return mutated


def generation(evo, pop):
    new_individuals = []
    for p in pop:
        for i in range(0, evo.lmbd // evo.mu):
            new_individuals.append(mutation(evo, p))
    missing = evo.lmbd - (evo.lmbd // evo.mu) * evo.mu
    for i in range(0, missing):
        new_individuals.append(mutation(evo, pop[i]))
    pop = sorted(pop + new_individuals, key=lambda x: mean_error(evo, x))
    return pop[0:evo.mu]


def initial_pop(evo):
    return [random_ruleset(evo) for i in range(0, evo.mu)]


def evolution_strategy(evo, save=100):
    pop = initial_pop(evo)
    best_fit = []
    for i in range(0, evo.generations):
        pop = generation(evo, pop)
        best_fit.append(mean_error(evo, pop[0]))
        if (i + 1) % save == 0:
            print(f"{i + 1}\t{mean_error(evo, pop[0])}")
    return pop, best_fit


def mean_error(evo, ruleset):
    err = 0
    n = len(evo.train_set)
    for before, after in evo.train_set:
        b = Membrane.clone(before)
        b.apply(ruleset)
        err += evo.distance(b, after)
    return err / n


def detailed_errors(evo, ruleset):
    err = 0
    n = len(evo.train_set)
    for before, after in evo.train_set:
        b = Membrane.clone(before)
        b.apply(ruleset, verbose=False)
        d = evo.distance(b, after)
        print(f"Input: {before}\nObtained: {b}\nExpected: {after}\nDist={d}\n")
        err += d
    return err / n
