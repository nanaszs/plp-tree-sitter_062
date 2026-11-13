import tree_sitter_python as tspython
from tree_sitter import Language, Parser

parser = Parser(Language(tspython.language()))

kode = b"if x > 1:\n    print(x)\nelse:\n    print(0)\n"
tree = parser.parse(kode)
print(tree.root_node)