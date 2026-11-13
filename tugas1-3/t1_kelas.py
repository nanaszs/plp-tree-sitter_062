import tree_sitter_python as tspython
from tree_sitter import Language, Parser

parser = Parser(Language(tspython.language()))

kode = b"class Hewan:\n    def suara(self):\n        return 'halo'\n"
tree = parser.parse(kode)
print(tree.root_node)