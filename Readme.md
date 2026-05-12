# Permata Bank Review Text Mining

Pipeline modular untuk mengambil ulasan aplikasi PermataMobile X dari Google Play Store, memberi label sentimen berdasarkan rating, membersihkan teks, normalisasi slang (lokal), penghapusan stopword (lokal), dan stemming (via GataFramework API). Proses berjalan paralel dengan logging progres.

## Fitur
- Scrape ulasan terbaru dengan `google-play-scraper`.
- Label otomatis berdasarkan rating (≤2 Negatif, 3 Netral, ≥4 Positif).
- Text cleaning (hapus URL, emotikon teks, hashtag, tanda baca, lowercasing, trim).
- Normalisasi slang pakai `slank.json` (lokal).
- Stopword removal pakai `stopword.json` (lokal).
- Stemming Bahasa Indonesia melalui GataFramework API (retry & logging).
- Proses paralel (ThreadPoolExecutor) + progress tracking.
- Output tersimpan ke folder `data/`.

## Prasyarat
- Python 3.8+ disarankan.
- Internet aktif (untuk scraping dan stemming via API).

## Instalasi
```bash
pip install -r google-play-scraper pandas openpyxl
```
Opsional (direkomendasikan): gunakan virtualenv/venv.

## Menjalankan
```bash
python index.py
```
Logging proses akan tampil di terminal, termasuk status panggilan API GataFramework dan progres baris yang diproses.

## Konfigurasi Utama
- ID aplikasi Play Store: ubah konstanta `APP_ID` di `modules/data_collection.py`.
- Jumlah ulasan/bahasa/negara: parameter `fetch_reviews_from_playstore(count=..., lang=..., country=...)` di `modules/data_collection.py` (dipanggil dari `modules/pipeline.py`).
- Jumlah worker paralel: ubah argumen `max_workers` saat memanggil `process_text_mining(...)` di `modules/pipeline.py` (default 4).
- Daftar slang: sunting `slank.json`.
- Daftar stopword: sunting `stopword.json`.

## Output
File hasil akan dibuat otomatis di folder `data/`:
- `bank-permata-data-set.csv` — hasil scraping mentah.
- `bank-permata-labeling-data-set.csv` — data setelah auto labeling.
- `bank-permata-labeling-data-set-result.xlsx` — hasil akhir (cleaning → slang removal → stopword removal → stemming).

Catatan: Direkomendasikan menambahkan folder `data/` ke `.gitignore` agar tidak ikut ter-commit.

## Arsitektur Modular (file utama)
```
.
├─ index.py                        # Entrypoint: memanggil pipeline
├─ modules/
│  ├─ pipeline.py                 # Orkestrasi seluruh langkah
│  ├─ logging_config.py           # Konfigurasi logger
│  ├─ data_collection.py          # Ambil ulasan dari Play Store
│  ├─ data_preparation.py         # Bentuk DataFrame & simpan CSV raw
│  ├─ labeling.py                 # Auto-label & simpan CSV label
│  ├─ dictionaries.py             # Load slang & stopword
│  ├─ text_preprocessing.py       # Pembersihan teks dasar
│  ├─ gata_api.py                 # Panggilan GataFramework (stemming)
│  └─ text_mining.py              # Proses per baris + paralel
├─ slank.json                     # Kamus slang → arti
├─ stopword.json                  # Daftar stopword
└─ data/                          # Output (dibuat otomatis)
```

## Troubleshooting
- API GataFramework gagal/time out:
  - Script akan retry otomatis dan menulis "time out" bila tetap gagal.
  - Cek koneksi internet atau jalankan ulang.
- Stopword/slang tidak terhapus:
  - Pastikan entri di `slank.json`/`stopword.json` huruf kecil (lowercase).
  - Stopword removal dilakukan sebelum stemming.
- Scraping kosong/kurang:
  - Naikkan nilai `count` atau jalankan ulang pada waktu berbeda.

## Lisensi
Digunakan untuk keperluan riset/pembelajaran internal.

