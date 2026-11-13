import sys
import tree_sitter_python as tspython
from tree_sitter import Language, Parser

parser = Parser(Language(tspython.language()))

def jelajah(node, kedalaman=0, field=None):
    baris, kolom = node.start_point
    label = f"{field}: " if field else ""
    print("  " * kedalaman + f"{label}{node.type} [{baris + 1}:{kolom}]")
    # TODO: untuk setiap child yang bernama, panggil jelajah() lagi
    #       dengan kedalaman + 1 dan nama field-nya.
    for i, child in enumerate(node.children):
        if not child.is_named:          # lewati node yang tidak bernama
            continue
        nama_field = node.field_name_for_child(i)
        jelajah(child, kedalaman + 1, nama_field)

with open(sys.argv[1], "rb") as f:
    tree = parser.parse(f.read())
jelajah(tree.root_node)