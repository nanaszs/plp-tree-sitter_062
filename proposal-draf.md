# Proposal Draf: Pendeteksi console.log di Kode Produksi JavaScript

## 1. Judul
Pendeteksi console.log di kode produksi aplikasi web dengan tree-sitter

## 2. Masalah
Developer sering lupa menghapus console.log yang dipakai untuk debugging. Jika terbawa ke produksi, log bisa membocorkan data (misalnya token atau data pengguna) dan membuat konsol browser berantakan. Reviewer sulit menemukannya satu per satu di basis kode yang besar.

## 3. Kenapa tidak cukup dengan AI saja
Tool tree-sitter hasilnya konsisten (input yang sama selalu memberi laporan yang sama), hampir tanpa biaya per pengecekan, dan bisa dijalankan otomatis di CI pada setiap commit. Regex akan salah menandai console.log yang ada di dalam komentar atau string, sedangkan tree-sitter paham struktur kode sehingga hanya menandai pemanggilan yang sebenarnya.

## 4. Bahasa dan grammar
JavaScript, grammar tree-sitter-javascript

## 5. Contoh kode
Harus terdeteksi:
console.log("debug");
Tidak boleh terdeteksi:
// console.log("debug")
const teks = "console.log";

## 6. Rancangan query
(call_expression
  function: (member_expression
    object: (identifier) @obj
    property: (property_identifier) @prop)
  (#eq? @obj "console")
  (#eq? @prop "log"))

## 7. Bentuk output
Laporan di terminal: nama file, nomor baris, dan potongan kodenya

## 8. Cara evaluasi
Tool dijalankan pada satu repositori open source JavaScript berukuran kecil. Dari hasilnya, 20 temuan dicek manual untuk menghitung berapa yang benar-benar pemanggilan console.log.

## 9. Rencana kerja dan risiko
Minggu 1: tulis query dan uji pada contoh kecil. Minggu 2: buat skrip yang menelusuri folder proyek. Minggu 3: uji pada repositori nyata dan cek manual. Minggu 4: rapikan laporan dan dokumentasi. Risiko: pemanggilan lewat alias (misalnya const log = console.log) tidak terdeteksi, dan itu dicatat sebagai batasan.
