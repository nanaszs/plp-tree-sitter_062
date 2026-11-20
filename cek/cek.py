import sys
from pathlib import Path
import tree_sitter_python as tspython
from tree_sitter import Language, Parser, Query, QueryCursor

PY = Language(tspython.language())
parser = Parser(PY)

Q_TODO = Query(PY, '((comment) @c (#match? @c "TODO|FIXME"))')
Q_FUNC = Query(PY, "(function_definition name: (identifier) @nama) @fungsi")

def cari_error(node):
    if node.is_error or node.is_missing:
        return node
    for c in node.children:
        hasil = cari_error(c)
        if hasil:
            return hasil
    return None

def cek_file(path):
    tree = parser.parse(path.read_bytes())

    # Fitur 1: komentar TODO/FIXME
    for node in QueryCursor(Q_TODO).captures(tree.root_node).get("c", []):
        print(f"{path}:{node.start_point[0] + 1}: {node.text.decode().strip()}")

    # Fitur 2: fungsi lebih dari 30 baris
    for _, cap in QueryCursor(Q_FUNC).matches(tree.root_node):
        f = cap["fungsi"][0]
        nama = cap["nama"][0].text.decode()
        baris = f.end_point[0] - f.start_point[0] + 1
        if baris > 30:
            print(f"{path}:{f.start_point[0] + 1}: fungsi {nama} terlalu panjang ({baris} baris)")

    # Fitur 3: file yang pohonnya error
    if tree.root_node.has_error:
        err = cari_error(tree.root_node)
        print(f"{path}:{err.start_point[0] + 1}: sintaks bermasalah")

for path in Path(sys.argv[1]).rglob("*.py"):
    if any(p in path.parts for p in ("venv", ".git", "node_modules")):
        continue
    cek_file(path)