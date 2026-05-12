# Permata Bank Review Text Mining

Pipeline sederhana untuk mengambil ulasan aplikasi PermataMobile X dari Google Play Store, melakukan pelabelan sentimen berdasarkan rating, pembersihan teks, normalisasi slang (lokal), penghapusan stopword (lokal), dan stemming (via GataFramework API). Hasil diproses paralel dan dilengkapi logging progres ke terminal.

## Fitur
- Scrape ulasan terbaru dengan `google-play-scraper`.
- Label otomatis berdasarkan rating (≤2 Negatif, 3 Netral, ≥4 Positif).
- Text cleaning (hapus URL, emotikon teks, hashtag, tanda baca, lowercasing, trim).
- Normalisasi slang pakai `slank.json` (lokal).
- Stopword removal pakai `stopword.json` (lokal).
- Stemming Bahasa Indonesia melalui GataFramework API (dengan retry & logging).
- Proses paralel (ThreadPoolExecutor) + progress tracking.
- Output tersimpan ke folder `data/`.

## Prasyarat
- Python 3.8+ disarankan.
- Internet aktif (untuk scraping dan stemming via API).

## Instalasi
```bash
pip install -r google-play-scraper pandas openpyxl
```

## Menjalankan
```bash
python index.py
```
Logging proses akan tampil di terminal, termasuk status panggilan API GataFramework dan progres row yang diproses.

## Konfigurasi Utama
- ID aplikasi Play Store: atur di `index.py` pada variabel `app_id`.
- Jumlah ulasan: atur argumen `count` pada pemanggilan `reviews(...)`.
- Bahasa/negara ulasan: `lang='id'`, `country='id'`.
- Jumlah worker paralel: parameter `max_workers` pada `rm_main(data, max_workers=4)`.
- Daftar slang: sunting `slank.json`.
- Daftar stopword: sunting `stopword.json`.

## Output
File hasil akan dibuat otomatis di folder `data/`:
- `bank-permata-data-set.csv` — dataset awal hasil scraping.
- `bank-permata-labeling-data-set.csv` — dataset dengan label sentimen.
- `bank-permata-labeling-data-set-result.xlsx` — hasil setelah cleaning → slang removal → stopword removal → stemming.

Catatan: Folder `data/` sudah di-`gitignore` agar tidak ikut ter-commit.

## Struktur Proyek (ringkas)
```
.
├─ index.py                     # Pipeline utama
├─ slank.json                  # Kamus slang → arti
├─ stopword.json               # Daftar stopword
├─ requirements.txt            # Dependensi Python
├─ .gitignore                  # Mengabaikan folder data/ dan lainnya
└─ data/                       # Output (dibuat otomatis)
```

## Troubleshooting
- API GataFramework gagal/time out:
	- Script akan retry otomatis dan menulis "time out" bila tetap gagal.
	- Cek koneksi internet atau coba jalankan ulang.
- Stopword/slang tidak terhapus:
	- Pastikan bentuk kata di `slank.json`/`stopword.json` huruf kecil (lowercase).
	- Proses stopword dilakukan sebelum stemming untuk akurasi.
- Scraping kosong/kurang:
	- Naikkan nilai `count` atau jalankan ulang pada waktu berbeda.

## Lisensi
Digunakan untuk keperluan riset/pembelajaran internal.

