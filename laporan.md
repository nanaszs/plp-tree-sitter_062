# Laporan Part 1 - Tree-sitter

## Tugas 1 - Membaca pohon

**Potongan yang dicoba:** 
`x = 1`, fungsi, `if/else`, dan kelas.

**Tebakan vs hasil:**
*Potongan `x = 1`*
- Tebakan saya: 
```text
module
  assignment
    x
    1
```
- Hasil sebenarnya:
```text
(module (expression_statement (assignment left: (identifier) right: (integer))))
```
- Perbandingan: Tebakan saya sebagian benar karena memang ada bagian untuk variabel x dan nilai 1. Namun saya belum mengetahui bahwa Tree-sitter menggunakan node expression_statement, assignment, identifier, dan integer.

*Potongan fungsi `def sapa(nama): return nama`*
- Tebakan saya: 
```text
module
  fungsi
    nama fungsi (sapa)
    parameter (nama)
    perintah mengembalikan nilai (nama)
```
- Hasil sebenarnya:
```text
(module (function_definition name: (identifier) parameters: (parameters (identifier)) body: (block (return_statement (identifier)))))
```
- Perbandingan: Tebakan saya memperkirakan bahwa fungsi memiliki nama, parameter, dan perintah di dalamnya. Namun, saya belum tau bagian-bagian tersebut akan dipecah menjadi node seperti function_definition, parameters, block, dan return_statement.

*Potongan `if/else`*
- Tebakan saya: 
```text
 if
    kondisi (x > 0)
    perintah jika benar
      print(x)
  else
    perintah jika salah
      print(0)
```
- Hasil sebenarnya:
```text
(module (if_statement condition: (comparison_operator (identifier) (integer)) consequence: (block (expression_statement (call function: (identifier) arguments: (argument_list (identifier))))) alternative: (else_clause body: (block (expression_statement (call function: (identifier) arguments: (argument_list (integer))))))))
```
- Perbandingan: 
Saya baru mengetahui bahwa pemanggilan print() memiliki node tersendiri, yaitu call.

*Potongan kelas dengan satu method*
- Tebakan saya: 
```text
module
  class
    nama kelas
    method
      nama method
      parameter
      perintah mengembalikan teks
```
- Hasil sebenarnya:
```text
(module (class_definition name: (identifier) body: (block (function_definition name: (identifier) parameters: (parameters(identifier)) body: (block (return_statement (string (string_start) (string_content) (string_end))))))))
```
- Perbandingan: 
Saya baru mengetahui method di dalam kelas tetap dibaca sebagai function_definition, juga teks yang dikembalikan oleh method dipecah menjadi beberapa bagian yaitu string_start, string_content, dan string_end.

**Node anonim yang ditemukan:**
Output dari `output_t1_anonim.txt`:
```text
def anonim
identifier bernama
parameters bernama
: anonim
block bernama
```

Node anonim yang terlihat adalah `def` dan `:`. Node bernama yang terlihat adalah `identifier`, `parameters`, dan `block`. Tanda kurung `(` dan `)` juga node anonim, tetapi tidak muncul di daftar ini karena program hanya mencetak anak langsung dari `function_definition`, sedangkan kurung berada satu tingkat lebih dalam, di dalam `parameters`.

**Perbedaan children dan named_children:**
`children` berisi semua anak sebuah node, termasuk yang anonim. `named_children` hanya berisi anak yang bernama. Pada `function_definition` dari kode fungsi tadi:
- `children` ada 5: `def`, `identifier`, `parameters`, `:`, `block`.
- `named_children` ada 3: `identifier`, `parameters`, `block`.

**Hasil saat kode dirusak:**
Titik dua (`:`) setelah `def sapa(nama)` sengaja dihapus. Hasilnya:
```text
(module (ERROR (identifier) (parameters (identifier)) (identifier)))
```
Node `function_definition` tidak terbentuk, dan seluruh isinya dibungkus node `ERROR`. Kata `return` juga tidak lagi menjadi `return_statement`. Pada percobaan ini yang muncul `ERROR`, bukan `MISSING`.

**Kendala dan cara mengatasinya:**
- Instalasi `nodejs` di Ubuntu (WSL) sempat gagal dengan pesan `Hash Sum mismatch`, karena satu file unduhan rusak. Saya mengatasinya dengan `sudo apt clean`, lalu `sudo apt update` dan install ulang. Setelah itu `node`, `npm`, dan `pip` terpasang.
- Output pohon berupa satu baris panjang sehingga sulit dibaca. Saya mencetak anak-anak node dengan perulangan `for` dan memeriksa `is_named` supaya node bernama dan anonim terlihat terpisah.

## Tugas 2 - Penjelajah node

**Yang dibuat:** tugas1-3/jelajah.py, fungsi rekursif yang mencetak node bernama dengan indentasi, posisi baris:kolom, dan nama field.

**Cara kerja:** Fungsi jelajah() menerima sebuah node, lalu mencetak tipenya beserta posisi baris:kolom dengan indentasi sesuai kedalaman. Setelah itu fungsi memeriksa semua anak dari node tersebut (node.children). Anak yang tidak bernama (is_named bernilai False) dilewati, sedangkan anak yang bernama diproses lagi dengan memanggil jelajah() dengan kedalaman ditambah 1. Nama field diambil dengan node.field_name_for_child(i), dengan i adalah urutan anak di dalam node.children, bukan di named_children. Karena fungsi memanggil dirinya sendiri, cara kerjanya sama seperti traversal DFS pada pohon.

**Hasil pada contoh fungsi:**

```text
module [1:0]
  function_definition [1:0]
    name: identifier [1:4]
    parameters: parameters [1:8]
      identifier [1:9]
    body: block [2:4]
      return_statement [2:4]
        identifier [2:11]
```

**Hasil pada file Python nyata** (textwrap.py bawaan Python, 475 baris, dipilih karena aman untuk repo Public). 20 baris pertama:

```text
module [1:0]
  expression_statement [1:0]
    string [1:0]
      string_start [1:0]
      string_content [1:3]
      string_end [2:0]
  comment [4:0]
  comment [5:0]
  comment [6:0]
  import_statement [8:0]
    name: dotted_name [8:7]
      identifier [8:7]
  expression_statement [10:0]
    assignment [10:0]
      left: identifier [10:0]
      right: list [10:10]
        string [10:11]
          string_start [10:11]
          string_content [10:12]
          string_end [10:23]
```

**Pengecekan:** Pada output file nyata, label field seperti name:, left:, dan right: muncul pada node yang memang punya field, dan indentasi bertambah satu tingkat setiap turun ke anak node, jadi sesuai dengan struktur kode. Posisi baris:kolom juga wajar, misalnya import_statement muncul di baris 8.

## Tugas 3 - Query pertama

**Hitungan manual pada contoh.py:** Dari isi contoh.py ada 2 fungsi (tambah dan kali) yang masing-masing punya 2 parameter, 1 pemanggilan print (di dalam kali), dan 2 import (os dan pathlib).

**Query nama fungsi (fungsi.scm):**

```scheme
(function_definition name: (identifier) @nama)
```

Hasil:

```text
@nama  baris 4: tambah
@nama  baris 7: kali
```

**Query pemanggilan print (print.scm):**

```scheme
(call
  function: (identifier) @fn
  arguments: (argument_list) @args
  (#eq? @fn "print"))
```

Hasil:

```text
@fn  baris 8: print
@args  baris 8: (a, b)
```

**Query import (import.scm):**

```scheme
(import_statement name: (dotted_name) @modul)
(import_from_statement module_name: (dotted_name) @modul)
```

Hasil:

```text
@modul  baris 1: os
@modul  baris 2: pathlib
```

**Jumlah parameter (params.scm dan q_params.py):**

```scheme
(function_definition name: (identifier) @nama parameters: (parameters) @params)
```

Hasil:

```text
tambah 2
kali 2
```

**Kesimpulan:** Semua hasil query cocok dengan hitungan manual: fungsi tambah (baris 4) dan kali (baris 7), print di baris 8, modul os dan pathlib, serta jumlah parameter tambah 2 dan kali 2.

## Tugas 4 - Grammar DSL filter

**Yang dibuat:** proyek tree-sitter-filter/ dengan grammar.js untuk DSL filter (perbandingan, and, or, not, kurung, in, contains).

**Penjelasan prioritas:** Rule or_expression dan and_expression memakai prec.left dengan angka prioritas. Operator and diberi angka 2 dan or diberi angka 1, sehingga and lebih kuat dan dikelompokkan lebih dulu, mirip perkalian yang dikerjakan lebih dulu daripada penjumlahan. Karena itu a = 1 or b = 2 and c = 3 dibaca sebagai a = 1 or (b = 2 and c = 3). Pada prec.left, jika ada operator yang sama berurutan, pengelompokannya dimulai dari kiri.

**Penjelasan in_expression dan contains_expression:** in_expression terdiri dari nama field, kata in, tanda kurung buka, satu nilai, lalu repeat(seq(',', nilai)) untuk nilai berikutnya, dan tanda kurung tutup. Dengan repeat, jumlah nilai dalam daftar bisa satu atau lebih. Setiap nilai diberi field value, sehingga di pohon muncul beberapa value. contains_expression lebih sederhana, yaitu nama field, kata contains, lalu satu nilai.

**Hasil parse pada contoh.filter:**

```text
(query [0, 0] - [0, 50]
  (or_expression [0, 0] - [0, 50]
    left: (comparison [0, 0] - [0, 15]
      field: (identifier [0, 0] - [0, 6])
      value: (string [0, 9] - [0, 15]))
    right: (and_expression [0, 19] - [0, 50]
      left: (comparison [0, 19] - [0, 31]
        field: (identifier [0, 19] - [0, 27])
        value: (number [0, 30] - [0, 31]))
      right: (comparison [0, 36] - [0, 50]
        field: (identifier [0, 36] - [0, 41])
        value: (string [0, 44] - [0, 50])))))
```

**Hasil tree-sitter test (7 tes):**

```text
  dasar:
      1. ✓ [32mperbandingan sederhana[0m
      2. ✓ [32moperator lebih besar sama dengan[0m
      3. ✓ [32mand lebih kuat dari or[0m
      4. ✓ [32mkurung mengubah urutan[0m
      5. ✓ [32mnot dan boolean[0m
      6. ✓ [32min dengan tiga nilai[0m
      7. ✓ [32mcontains[0m

Total parses: 7; successful parses: 7; failed parses: 0; success percentage: 100.00%; average speed: 3641 bytes/ms

```

**Kendala:** grammar.js dengan module.exports gagal saat generate. Detailnya ada di catatan penggunaan AI di bawah.

## Tugas 5 - Highlight untuk DSL filter

**queries/highlights.scm:**

```scheme
["and" "or" "not" "in" "contains"] @keyword
["=" "!=" ">" "<" ">=" "<="] @operator
(string) @string
(number) @number
(boolean) @constant.builtin
(comparison field: (identifier) @property)
(in_expression field: (identifier) @property)
(contains_expression field: (identifier) @property)
```

**Hasil tree-sitter highlight contoh2.filter:** Di terminal, kata kunci (in, and, not, or, contains) berwarna ___, string berwarna ___, boolean (true) berwarna ___, dan nama field (status, archived, title) berwarna ___. Tiap jenis token punya warna berbeda sesuai highlights.scm.

**Kendala:** muncul Warning karena tree-sitter.json belum punya entry highlights. Detailnya ada di catatan penggunaan AI di bawah.

## Tugas 6 - Pendeteksi TODO, fungsi panjang, dan file error

**Yang dibuat:** cek/cek.py, README ada di cek/README.md.

**Cara kerja:** cek.py membaca setiap file .py di folder yang diberikan lalu mem-parse-nya. Fitur 1 memakai query comment dengan predikat #match? untuk mencari komentar yang berisi TODO atau FIXME. Fitur 2 memakai query function_definition, lalu menghitung panjang fungsi dari end_point dikurangi start_point ditambah 1, dan melaporkannya jika lebih dari 30 baris. Fitur 3 memeriksa tree.root_node.has_error. Jika hasilnya True, fungsi cari_error menelusuri pohon secara rekursif untuk mencari node ERROR atau MISSING pertama, lalu melaporkan barisnya.

**Hasil pada folder uji (cek/uji/):**

```text
cek/uji/todo.py:1: # TODO: rapikan fungsi ini
cek/uji/panjang.py:1: fungsi panjang terlalu panjang (37 baris)
cek/uji/rusak.py:1: sintaks bermasalah
```

**Hasil pada repo nyata** (pallets/itsdangerous):

```text
/tmp/itsdangerous/src/itsdangerous/url_safe.py:23: fungsi load_payload terlalu panjang (31 baris)
/tmp/itsdangerous/src/itsdangerous/timed.py:182: # TODO: Signature is incompatible because parameters were added
/tmp/itsdangerous/src/itsdangerous/timed.py:72: fungsi unsign terlalu panjang (87 baris)
/tmp/itsdangerous/src/itsdangerous/timed.py:185: fungsi loads terlalu panjang (36 baris)
/tmp/itsdangerous/src/itsdangerous/signer.py:129: fungsi __init__ terlalu panjang (45 baris)
/tmp/itsdangerous/src/itsdangerous/signer.py:182: fungsi derive_key terlalu panjang (32 baris)
/tmp/itsdangerous/src/itsdangerous/serializer.py:190: fungsi __init__ terlalu panjang (45 baris)
```

**Pengecekan manual pada 2 file acak:** Saya membuka timed.py dan signer.py. Di timed.py, fungsi unsign (baris 72, 87 baris) dan loads (baris 185, 36 baris) memang ada dan melebihi 30 baris. Di signer.py, __init__ (baris 129, 45 baris) dan derive_key (baris 182, 32 baris) juga cocok. Temuan TODO di timed.py baris 182 juga ada di file. Semua temuan cocok.

## Catatan penggunaan AI

- **Yang aku minta ke AI:** Dipandu langkah demi langkah untuk setup (WSL, git, virtual environment, tree-sitter), dijelaskan hasil output Tugas 1, dibantu menyusun kerangka laporan, serta diberi kode contoh untuk q.py, query .scm, cek.py, grammar.js, file tes, dan highlights.scm yang saya jalankan dan cocokkan dengan hasilnya. Penjelasan cara kerja kode di laporan ini juga sempat dibantu AI, lalu saya baca ulang dan tulis ulang dengan bahasa sendiri.
- **Kesalahan 1 dari AI:** grammar.js yang diberikan memakai module.exports. Saat tree-sitter generate muncul error ReferenceError: module is not defined in ES module scope, karena package.json hasil tree-sitter init berisi type module. Cara membuktikannya: pesan error dari generate, lalu setelah baris pertama diganti menjadi export default grammar, generate berhasil dan 7 tes lulus.
- **Kesalahan 2 dari AI:** AI menyebut bahwa entry highlights di tree-sitter.json tidak perlu karena CLI membaca queries/highlights.scm otomatis. Kenyataannya muncul Warning agar menambahkan entry highlights. Cara membuktikannya: Warning muncul di output tree-sitter highlight, lalu hilang setelah saya menambahkan highlights dengan nilai queries/highlights.scm di tree-sitter.json (commit Tugas 5).
- **Cara aku memverifikasi hasil AI secara umum:** setiap kode saya jalankan, outputnya disimpan ke file .txt, dan dibandingkan dengan hitungan atau tebakan manual.
