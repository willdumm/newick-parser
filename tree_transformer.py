from lark import Transformer, Lark
from lark.visitors import Discard
import ete3

class TreelistTransformer(Transformer):

    list = list

    def integer(self, s):
        (s,) = s
        return int(s)

    def float(self, s):
        (s,) = s
        return float(s)

    def string(self, s):
        (s,) = s
        return str(s)

    def support(self, s):
        return [('dist',s[0])]

    def quoted_escaped_string(self, s):
        (value,) = s
        return str(value[1:-1])

    def annotationname(self, s):
        return str(s[0])

    def annotation(self, s):
        return tuple(s)

    def annotationlist(self, s):
        return list(s)

    def internal_node(self, s):
        return self.leaf_node(s)

    def leaf_node(self, s):
        n = ete3.TreeNode()
        for parse_child in s:
            if parse_child.data == 'children':
                for child in parse_child.children:
                    n.add_child(child=child)
            elif parse_child.data == 'annotations':
                n.add_features(**dict(t for child in parse_child.children for t in child))
            elif parse_child.data == 'nodename':
                n.name = str(parse_child.children[0])
        return n


class NexusTransformer(TreelistTransformer):

    def pair(self, s):
        return tuple(s)

    def taxon_name(self, s):
        return str(s[0])

    def leaf_mapping(self, s):
        leaf_map = dict(s)
        self.leaf_map = leaf_map
        return Discard


    def leaf_node(self, s):
        n = ete3.TreeNode()
        for parse_child in s:
            if parse_child.data == 'children':
                for child in parse_child.children:
                    n.add_child(child=child)
            elif parse_child.data == 'annotations':
                n.add_features(**dict(t for child in parse_child.children for t in child))
            elif parse_child.data == 'nodename':
                n.name = self.leaf_map[int(parse_child.children[0])]
        return n

    def beast_tree(self, s):
        tree = s[-1]
        tree.add_feature("beast_name", s[0])
        tree.add_feature("beast_annotations", dict(s[1]))
        tree.add_feature("rice_annotation", s[2])
        return tree

    def beast_file(self, s):
        return s[1]

with open('newick.lark', 'r') as fh:
    _nexus_parser = Lark(fh, parser='lalr', start='beast_file', transformer=NexusTransformer())

with open('newick.lark', 'r') as fh:
    _newick_parser = Lark(fh, parser='lalr', start='newicklist', transformer=TreelistTransformer())

def parse_newick(data):
    """Parse a string containing concatenated newick strings.

    Returns a list of ete3.Tree objects containing the parsed trees."""
    return _newick_parser.parse(data)

def parse_newick_file(filepath):
    """Parse a file containing newick strings.

    Returns a list of ete3.Tree objects containing the parsed trees."""
    with open(filepath, 'r') as fh:
        return _newick_parser.parse(fh.read())

def parse_nexus_file(filepath):
    """Parse a nexus file output by Beast.

    Returns a list of ete3.Tree objects containing the parsed trees. Leaves have taxon names in the ``name`` attribute, and
    tree root nodes have ``beast_name``, ``beast_annotations``, and ``rice_annotation`` attributes containing tree annotations.
    All other extended newick annotations are saved in the corresponding attribute on each node."""
    with open(filepath, 'r') as fh:
        for line in fh:
            if "Begin trees;" in line:
                data = fh.read()
    return _nexus_parser.parse(data)
