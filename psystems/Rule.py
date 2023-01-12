from enum import Enum
import multiset as ms

from psystems.Membrane import Membrane


class RuleType(Enum):
    EVOLUTION = 1
    SEND_IN = 2
    SEND_OUT = 3
    DIVISION = 4


class Rule:

    def __init__(self, lhs, rhs, label, rule_type):
        self.lhs = ms.Multiset(lhs)
        self.rhs = list(map(ms.Multiset, rhs))
        self.label = label
        self.rule_type = rule_type

    @classmethod
    def from_string(cls, string):
        label, str_lhs, str_rule_type, str_rhs = tuple(string.split(' '))
        rule_type = RuleType[str_rule_type.upper()]
        lhs = str_lhs.replace('{', '').replace('}', '').split('/')
        rhs = [li.split('/') for li in str_rhs.replace('}{', '-').replace('{', '').replace('}', '').split('-')]
        return Rule(lhs, rhs, label, rule_type)

    def apply(self, membrane, verbose=False):
        if self.rule_type == RuleType.EVOLUTION:
            if self.lhs <= membrane.content and membrane.label == self.label:
                membrane.content -= self.lhs
                membrane.new_content += self.rhs[0]
                if verbose:
                    print(f"{self} applied")
                return True
        elif self.rule_type == RuleType.SEND_IN:
            if self.lhs <= membrane.content:
                for m in membrane.children:
                    if not m.blocked and m.label == self.label:
                        m.new_content += self.rhs[0]
                        membrane.content -= self.lhs
                        m.blocked = True
                        if verbose:
                            print(f"{self} applied")
                        return True
        elif self.rule_type == RuleType.SEND_OUT:
            if (not membrane.blocked and
                    self.lhs <= membrane.content and
                    membrane.label == self.label and
                    membrane.parent is not None):
                membrane.content -= self.lhs
                membrane.parent.new_content += self.rhs[0]
                membrane.blocked = True
                if verbose:
                    print(f"{self} applied")
                return True
        elif self.rule_type == RuleType.DIVISION:
            if (not membrane.blocked and
                    self.lhs <= membrane.content and
                    membrane.label == self.label and
                    membrane.parent is not None):
                membrane.content -= self.lhs
                membrane.blocked = True
                m = Membrane.clone(membrane)
                membrane.new_content += self.rhs[0]
                m.new_content += self.rhs[1]
                m.parent.new_membranes += [m]
                if verbose:
                    print(f"{self} applied")
                return True
        else:
            raise ValueError("Invalid rule type")
        return False

    def __str__(self):
        if self.rule_type == RuleType.EVOLUTION:
            return f"[{self.lhs} -> {self.rhs[0]}]_{self.label}"
        elif self.rule_type == RuleType.SEND_IN:
            return f"{self.lhs} -> [{self.rhs[0]}]_{self.label}"
        elif self.rule_type == RuleType.SEND_OUT:
            s = f"[{self.lhs}]_{self.label} -> []_{self.label} {self.rhs[0]}"
            return s
        elif self.rule_type == RuleType.DIVISION:
            s = f"[{self.lhs}]_{self.label} -> [{self.rhs[0]}]_{self.label}"
            s += f" [{self.rhs[1]}]_{self.label}"
            return s
        raise ValueError("Invalid rule type")

    def __repr__(self):
        return str(self)
