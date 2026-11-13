import tree_sitter_python as tspython
from tree_sitter import Language, Parser

parser = Parser(Language(tspython.language()))

kode = b"def sapa(nama)\n    return nama\n"
tree = parser.parse(kode)
print(tree.root_node)

for c in tree.root_node.children[0].children:
    print(c.type, "bernama" if c.is_named else "anonim")