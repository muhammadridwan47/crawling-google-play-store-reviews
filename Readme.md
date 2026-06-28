# 📱 Crawling Google Play Store Reviews

Aplikasi sederhana untuk mengambil dan menganalisis review dari Google Play Store (Permata Bank Mobile X). Semua kode ditulis dalam **satu file** (`index.py`) yang mudah dibaca dan dipahami, bahkan oleh pemula!

## ✨ Fitur Utama

- 🔍 **Scraping Review** - Mengambil review terbaru dari Google Play Store
- 🏷️ **Auto Labeling** - Memberikan label sentimen otomatis:
  - ⭐⭐ (Rating 1-2) → **Negatif**
  - ⭐⭐⭐ (Rating 3) → **Netral**
  - ⭐⭐⭐⭐⭐ (Rating 4-5) → **Positif**
- 🧹 **Text Cleaning** - Membersihkan teks dari URL, emoticon, hashtag, dan karakter khusus
- 💬 **Normalisasi Slang** - Mengubah kata slang menjadi kata baku (contoh: "gue" → "saya")
- 🚫 **Stopword Removal** - Menghapus kata-kata yang tidak penting
- 🌿 **Stemming** - Mengubah kata ke bentuk dasarnya via GataFramework API
- ⚡ **Proses Paralel** - Pemrosesan cepat dengan multi-threading
- 📊 **Export Excel** - Hasil tersimpan dalam format Excel yang rapi

## 📋 Prasyarat

- Python 3.8 atau lebih baru
- Koneksi internet (untuk scraping dan API stemming)

## 🚀 Instalasi

1. **Install dependencies:**
```bash
pip install google-play-scraper pandas openpyxl
```

2. **Atau gunakan Makefile:**
```bash
make install
```

💡 **Tip:** Gunakan virtual environment untuk isolasi package:
```bash
python -m venv venv
source venv/bin/activate  # Mac/Linux
# atau
venv\Scripts\activate     # Windows
```

## 🎯 Cara Menggunakan

### Metode 1: Langsung dengan Python
```bash
python index.py
```

### Metode 2: Menggunakan Makefile
```bash
make run
```

Program akan menampilkan progress di terminal, termasuk:
- Status pengambilan review
- Progress pemrosesan setiap baris
- Status panggilan API GataFramework
- Hasil akhir

## ⚙️ Konfigurasi

Semua konfigurasi ada di file `index.py`. Anda bisa mengubah:

### 1. **ID Aplikasi Play Store**
```python
APP_ID = 'net.myinfosys.PermataMobileX'  # Ubah sesuai aplikasi yang ingin di-crawl
```

### 2. **Jumlah Review yang Diambil**
```python
# Di fungsi fetch_reviews_from_playstore()
def fetch_reviews_from_playstore(count=10, lang='id', country='id'):
    # Ubah count=10 menjadi jumlah yang diinginkan
```

### 3. **Jumlah Worker Paralel**
```python
# Di fungsi main()
processed_df = process_text_mining(labeled_data, slank_dict, stopword_set, max_workers=4)
# Ubah max_workers=4 sesuai kemampuan komputer Anda
```

### 4. **Kamus Slang**
Edit file `slank.json` untuk menambah/mengubah kata slang:
```json
[
  {"slank": "gue", "slankmean": "saya"},
  {"slank": "gak", "slankmean": "tidak"}
]
```

### 5. **Daftar Stopword**
Edit file `stopword.json` untuk menambah/mengubah stopword:
```json
["yang", "di", "ke", "dari", "untuk"]
```

## 📁 Struktur File

```
📦 crawling-google-play-store-reviews/
├── 📄 index.py              # ⭐ SEMUA KODE ADA DI SINI (file utama)
├── 📄 slank.json            # Kamus kata slang → kata baku
├── 📄 stopword.json         # Daftar stopword bahasa Indonesia
├── 📄 Makefile              # Perintah make untuk kemudahan
├── 📄 Readme.md             # Dokumentasi ini
└── 📁 data/                 # Folder hasil (dibuat otomatis)
    ├── bank-permata-data-set.csv                    # Data mentah hasil scraping
    ├── bank-permata-labeling-data-set.csv           # Data setelah labeling
    └── bank-permata-labeling-data-set-result.xlsx   # ✅ Hasil akhir (Excel)
```

## 📊 Output yang Dihasilkan

Semua file hasil akan tersimpan otomatis di folder `data/`:

| File | Deskripsi |
|------|-----------|
| `bank-permata-data-set.csv` | Data mentah hasil scraping dari Play Store |
| `bank-permata-labeling-data-set.csv` | Data setelah diberi label sentimen |
| `bank-permata-labeling-data-set-result.xlsx` | **Hasil akhir** dengan semua proses text mining |

### Kolom di File Hasil Akhir:
- `no` - Nomor urut
- `ulasan` - Review asli
- `rating` - Rating (1-5)
- `tanggal` - Tanggal review
- `label` - Sentimen (Positif/Netral/Negatif)
- `slang` - Teks setelah normalisasi slang
- `indonesian_stopword_removal` - Teks setelah hapus stopword
- `indonesian_stemming` - Teks setelah stemming

## 🔧 Troubleshooting

### ❌ API GataFramework Gagal/Time Out
**Solusi:**
- Script akan retry otomatis 3x
- Jika tetap gagal, akan menulis "time out"
- Cek koneksi internet Anda
- Coba jalankan ulang program

### ❌ Stopword/Slang Tidak Terhapus
**Solusi:**
- Pastikan entri di `slank.json` dan `stopword.json` dalam huruf kecil
- Stopword removal dilakukan sebelum stemming
- Periksa format JSON tidak rusak

### ❌ Scraping Kosong/Kurang dari yang Diharapkan
**Solusi:**
- Naikkan nilai parameter `count` di fungsi `fetch_reviews_from_playstore()`
- Jalankan ulang pada waktu berbeda
- Pastikan APP_ID benar
- Cek koneksi internet

### ❌ Error Import Module
**Solusi:**
```bash
pip install --upgrade google-play-scraper pandas openpyxl
```

## 📖 Penjelasan Alur Program

Program berjalan dalam **6 langkah** berurutan:

1. **LANGKAH 1** - Mengambil review dari Google Play Store
2. **LANGKAH 2** - Menyiapkan data dalam bentuk tabel (DataFrame)
3. **LANGKAH 3** - Memberikan label sentimen otomatis berdasarkan rating
4. **LANGKAH 4** - Memuat kamus slang dan stopword dari file JSON
5. **LANGKAH 5** - Memproses text mining (cleaning, slang removal, stopword removal, stemming)
6. **LANGKAH 6** - Menyimpan hasil akhir ke file Excel

Setiap langkah akan menampilkan progress dan status di terminal! 📺

## 🎓 Cocok untuk Pemula

File `index.py` ditulis dengan:
- ✅ Komentar lengkap dalam Bahasa Indonesia
- ✅ Struktur kode yang jelas dan terorganisir
- ✅ Nama fungsi dan variabel yang mudah dipahami
- ✅ Penjelasan setiap langkah proses
- ✅ Tidak ada struktur kompleks atau pattern advanced

## 📝 Catatan Penting

- Folder `data/` akan dibuat otomatis saat pertama kali menjalankan program
- Disarankan menambahkan `data/` ke `.gitignore` agar hasil tidak ikut ter-commit
- API GataFramework adalah layanan eksternal, pastikan koneksi internet stabil
- Proses stemming membutuhkan waktu karena memanggil API eksternal

## 📜 Lisensi

Digunakan untuk keperluan riset dan pembelajaran.

## 🤝 Kontribusi

Jika menemukan bug atau ingin menambah fitur, silakan buat issue atau pull request!

---

**Dibuat dengan ❤️ untuk pembelajaran text mining dan analisis sentimen**

