"""
2 example tree that we use as input to calculate the distance
"""
from anytree import Node as Node_at
from anytree import RenderTree


def print_at_tree(tree):
    for pre, fill, node in RenderTree(tree):
        print("%s%s" % (pre, node.name))


h1 = Node_at('a')  # also the indicator oof the first tree
h2 = Node_at('w', parent=h1)
h4 = Node_at('z', parent=h2)
h6 = Node_at('ab', parent=h4)
h7 = Node_at('u', parent=h4)
h5 = Node_at('c', parent=h2)
h3 = Node_at('p', parent=h1)


g1 = Node_at('a')  # also the indicator oof the second tree
g2 = Node_at('p', parent=g1)
g3 = Node_at('w', parent=g1)
g4 = Node_at('c', parent=g3)
g5 = Node_at('z', parent=g3)
g6 = Node_at('ba', parent=g5)
g7 = Node_at('u', parent=g5)


