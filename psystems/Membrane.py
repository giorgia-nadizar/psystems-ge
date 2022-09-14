import multiset as ms


class Membrane:

    def __init__(self, label, content, parent=None):
        self.label = label
        self.content = ms.Multiset(content)
        self.new_content = ms.Multiset()
        self.new_membranes = []
        self.parent = parent
        self.children = []
        self.blocked = False

    @classmethod
    def clone(cls, m):
        m_clone = cls(m.label, ms.Multiset(m.content), m.parent)
        m_clone.children = list(map(cls.clone, m.children))
        for m in m_clone.children:
            m.parent = m_clone
        m_clone.blocked = m.blocked
        m_clone.new_content = ms.Multiset(m.new_content)
        m_clone.new_membranes = list(map(cls.clone, m.new_membranes))
        for m in m_clone.new_membranes:
            m.parent = m_clone
        return m_clone

    def apply(self, ruleset, verbose=False):
        for m in self.children:
            m.apply(ruleset, verbose)
        for m in self.new_membranes:
            m.apply(ruleset, verbose)
        for r in ruleset:
            while r.apply(self, verbose):
                pass
        for m in self.children:
            m._reset()
        for m in self.new_membranes:
            m._reset()
        self._reset()

    def _reset(self):
        self.content += self.new_content
        self.new_content = ms.Multiset()
        self.children += self.new_membranes
        self.new_membranes = []
        self.blocked = False

    def distance(self, other):
        if self.label == other.label:
            intersection = self.content & other.content
            union = self.content | other.content
            if len(union) > 0:
                js = len(intersection) / len(union)
            else:
                js = 1
            dist = 1 - js
        else:
            dist = 1
        labels = set([m.label for m in self.children + other.children])
        for lbl in labels:
            m_self = [m for m in self.children if m.label == lbl]
            m_other = [m for m in other.children if m.label == lbl]
            m_self = sorted(m_self, key=lambda x: x._str_content())
            m_other = sorted(m_other, key=lambda x: x._str_content())
            for m1, m2 in zip(m_self, m_other):
                dist += m1.distance(m2)
            empty = Membrane("", "", None)
            if len(m_self) > len(m_other):
                for m in m_self[len(m_other):]:
                    dist += m.distance(empty)
            if len(m_other) > len(m_self):
                for m in m_other[len(m_self):]:
                    dist += m.distance(empty)
        return dist

    def _str_content(self):
        lst = [x for x in self.content]
        return str(sorted(lst))

    def __str__(self):
        s = f"[{self.content}"
        for m in self.children:
            s += " " + str(m)
        s += f"]_{self.label}"
        return s

    def __repr__(self):
        return str(self)

# h = Membrane("h", "aab", None)
# k = Membrane("k", "aaabbbcc", h)
# ell = Membrane("l", "bbc", h)
# h.children = [k, ell]

# rules = [Rule("a", ["aa"], "h", RuleType.EVOLUTION),
#          Rule("ab", ["bb"], "h", RuleType.EVOLUTION),
#          Rule("abc", ["d"], "k", RuleType.EVOLUTION),
#          Rule("b", ["e"], "l", RuleType.SEND_IN),
#          Rule("bb", ["a"], "l", RuleType.SEND_OUT),
#          Rule("a", ["b", "c"], "k", RuleType.DIVISION)]
