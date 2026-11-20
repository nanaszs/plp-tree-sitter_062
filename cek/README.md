# cek.py

CLI kecil untuk memeriksa file Python dengan tree-sitter.

## Cara pasang
```
pip install tree-sitter tree-sitter-python
```

## Cara menjalankan
```
python cek/cek.py <folder>
```

## Yang dilaporkan
- Komentar yang mengandung TODO atau FIXME
- Fungsi yang lebih dari 30 baris (semua fungsi dihitung, termasuk method dan fungsi bersarang)
- File yang pohonnya mengandung error sintaks

## Contoh output
```
cek/uji/todo.py:1: # TODO: rapikan fungsi ini
cek/uji/panjang.py:1: fungsi panjang terlalu panjang (37 baris)
cek/uji/rusak.py:1: sintaks bermasalah
```