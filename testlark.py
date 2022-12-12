from lark import Lark

nwks = [
    "((A,B),C)D;",
    "((,),);",
    "((A:1,B)E:1.0,C)D;",
    ("((A:1,B)E:[&NHX:rate=1:one=2]1.0,C)D;\n"
    "((A:1,B)E:[&NHX:rate={1,2,{2,3}}:one=2|4]1.0,C)D;"),
    "\"England/CAMC-B515AC/2020|2020-11-08\":1;",
    "England/CAMC-B515AC/2020|2020-11-08:1;",
    "((one:1[&&NHX:list=1|2|3:set=1|2|3:tuple=1|2|3],B));",
    '"node1"[&&NHX:list={1,2,3}:string=string_val:nested_list={1,2,[2, 3, [3, 4]]}:tuple={1,2,3}:set={1, 2, 3}:float=1.2345656777:nested_tuple={(1, 2),(2, 3)}];',
]

with open('newick.lark.ebnf', 'r') as fh:
    # newick_parser = Lark(fh, parser='lalr')
    newick_parser = Lark(fh, debug=True)

for nwk in nwks:
    print()
    print(nwk)
    print("was parsed as:")
    print(newick_parser.parse(nwk).pretty())
