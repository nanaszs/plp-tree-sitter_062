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

## Catatan penggunaan AI
- **Yang aku minta ke AI:** Dijelaskan hasil output Tugas 1 dan perbedaan `children` dengan `named_children`.
- **Kesalahan atau kekurangan hasil AI yang kutemukan:** Pada Tugas 1 belum ada kesalahan yang saya temukan. Penjelasan AI saya cocokkan dengan output program. 
- **Cara aku membuktikannya:** Saya menjalankan `t1_anonim.py`, menyimpan hasilnya ke `output_t1_anonim.txt`, lalu membandingkan daftar anak `function_definition` dengan pohon yang dicetak Tree-sitter.