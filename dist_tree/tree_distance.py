"""
given 2 trees the edit distance between them is calculated.
The distance node to node is computed by using the Jaccard index.
"""
import zss
import anytree as at
import collections as ct
from example_tree import *


def sort_tree(tree):
    """
    Implementation of a function that order the sons of every node (to make easier to compute the distance)
    :param tree: tree to order
    :return: ordered tree
    """
    if tree.children == ():
        return at.Node(tree.name)
    sons = list(tree.children)
    name_sons = [k.name for k in sons]
    zipped_list = zip(name_sons, sons)
    sorted_pairs = sorted(zipped_list)
    tuples = zip(*sorted_pairs)
    name_sons, sons = [list(tuple) for tuple in tuples]
    a_son = sons[0]
    this_root = at.Node(a_son.parent.name)
    this_root.children = [sort_tree(son) for son in sons]
    return this_root


def order_lessicogr(_str):
    """
    function that take a string as input and return the ordered string (according to lexicographic order)
    :param _str: input string
    :return: input string reordered
    """
    sorted_character = sorted(_str)
    _str = ''.join(sorted_character)
    return _str


def jaccard(str1, str2):
    """
    given two string the Jaccard distance is computed
    :param str1: first input string
    :param str2: second input string
    :return: Jaccard distance between str1 and str2
    """
    str1 = ct.Counter(str1)
    str2 = ct.Counter(str2)
    union = str1 | str2
    intersection = str1 & str2
    union_size = len(sorted(union))
    intersection_size = len(sorted(intersection))
    coeff_sim = intersection_size / union_size
    jaccard_dist = 1 - coeff_sim
    return jaccard_dist


try:
    from editdist import distance as strdist
except ImportError:
    def jaccard_node_distance(a, b):
        if a == b:
            return 0
        else:
            return jaccard(a, b)


def jaccard_dist(A, B):
    return jaccard_node_distance(A, B)


class JaccardNode(object):

    def __init__(self, label, my_children=None):
        self.my_label = label
        self.my_children = my_children or list()

    @staticmethod
    def get_children(node):
        return node.my_children

    @staticmethod
    def get_label(node):
        return node.my_label

    def addkid(self, node, before=False):
        if before:  self.my_children.insert(0, node)
        else:   self.my_children.append(node)
        return self


def at_to_zss(at_tree_root):
    """
    recursive function to transform a anytree type of tree (where we are able to perform ordering of the tree)
    in zss type of tree (where we are able to compute edit + Jaccard distance between trees)
    :param at_tree_root: tree in anytree format
    :return: tree in zss format
    """
    if at_tree_root.children == ():
        return JaccardNode(order_lessicogr(at_tree_root.name))
    sons = list(at_tree_root.children)
    first_son = sons[0]
    res = JaccardNode(order_lessicogr(first_son.parent.name), [at_to_zss(son) for son in sons])
    return res


def preparation_tree(tree):
    """
    Aggregation of all the functions defined above
    :param tree: anytree tree
    :return: zss ordered tree
    """
    print('original shape of the tree :')
    print_at_tree(tree)
    print('sorted tree :')
    tree = sort_tree(tree)
    print_at_tree(tree)
    tree_zss = at_to_zss(tree)
    return tree_zss


h1_zss = preparation_tree(h1)
g1_zss = preparation_tree(g1)

dist = zss.simple_distance(h1_zss, g1_zss, JaccardNode.get_children, JaccardNode.get_label, jaccard_dist)
print('Jaccard sistance between tree1 and tree2 : ', dist)
