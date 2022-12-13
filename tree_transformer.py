from lark import Transformer
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

    def node(self, s):
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



