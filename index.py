"""
========================================
CRAWLING GOOGLE PLAY STORE REVIEWS
Aplikasi untuk mengambil dan menganalisis review dari Google Play Store
========================================
"""

# ============================================================================
# IMPORT LIBRARY YANG DIBUTUHKAN
# ============================================================================
import os
import re
import json
import time
import logging
import urllib.parse
import urllib.request
import pandas as pd
from google_play_scraper import reviews, Sort
from concurrent.futures import ThreadPoolExecutor, as_completed


# ============================================================================
# KONFIGURASI LOGGING (untuk menampilkan progress)
# ============================================================================
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger("permata_pipeline")


# ============================================================================
# KONFIGURASI APLIKASI
# ============================================================================
APP_ID = 'net.myinfosys.PermataMobileX'  # ID aplikasi Permata Bank di Play Store
GATA_API_URL = "http://www.gataframework.com/textmining/index.php?model=transaction_text&action=processTextPublic&techniques="


# ============================================================================
# FUNGSI 1: MENGAMBIL REVIEW DARI GOOGLE PLAY STORE
# ============================================================================
def fetch_reviews_from_playstore(count_data=10, lang='id', country='id'):
    """
    Mengambil review dari Google Play Store
    
    Parameter:
    - count_data: jumlah review yang ingin diambil
    - lang: bahasa review (default: 'id' untuk Indonesia)
    - country: negara (default: 'id' untuk Indonesia)
    """
    logger.info("Mengambil review dari Google Play Store...")
    result, _ = reviews(
        APP_ID,
        lang=lang,
        country=country,
        sort=Sort.NEWEST,
        count=count_data,
    )
    logger.info(f"✓ Berhasil mengambil {len(result)} review")
    return result


# ============================================================================
# FUNGSI 2: MENYIAPKAN DATA DALAM BENTUK TABEL
# ============================================================================
def prepare_dataframe(raw_reviews):
    """
    Mengubah data mentah menjadi tabel yang rapi
    """
    logger.info("Menyiapkan data dalam bentuk tabel...")
    df = pd.DataFrame(raw_reviews)
    df = df[['content', 'score', 'at']]
    df.columns = ['ulasan', 'rating', 'tanggal']
    df['no'] = range(1, len(df) + 1)
    cols = ['no'] + [c for c in df.columns if c != 'no']
    df = df[cols]
    df['label'] = ""
    logger.info(f"✓ Data berhasil disiapkan: {len(df)} baris")
    return df


def save_raw_data(df, path='data/bank-permata-data-set.csv'):
    """
    Menyimpan data mentah ke file CSV
    """
    os.makedirs('data', exist_ok=True)
    df.to_csv(path, index=False)
    logger.info(f"✓ Data mentah disimpan ke: {path}")


# ============================================================================
# FUNGSI 3: MEMBERIKAN LABEL OTOMATIS BERDASARKAN RATING
# ============================================================================
def auto_label_data(data):
    """
    Memberikan label pada review:
    - Rating 1-2: Negatif
    - Rating 3: Netral
    - Rating 4-5: Positif
    """
    logger.info("Memberikan label otomatis berdasarkan rating...")
    label = []
    for _, row in data.iterrows():
        if row["rating"] <= 2:
            label.append("Negatif")
        elif row["rating"] == 3:
            label.append("Netral")
        else:
            label.append("Positif")
    data["label"] = label
    logger.info(f"✓ Labeling selesai: {len(data)} baris diberi label")
    return data


def save_labeled_data(data, path='data/bank-permata-labeling-data-set.csv'):
    """
    Menyimpan data yang sudah diberi label
    """
    data.to_csv(path, index=False)
    logger.info(f"✓ Data berlabel disimpan ke: {path}")


# ============================================================================
# FUNGSI 4: MEMUAT KAMUS SLANG DAN STOPWORD
# ============================================================================
def load_dictionaries(slank_path='slank.json', stopword_path='stopword.json'):
    """
    Memuat kamus kata slang dan daftar stopword dari file JSON
    """
    logger.info("Memuat kamus slang dan stopword...")
    
    # Memuat kamus slang
    with open(slank_path, 'r', encoding='utf-8') as f:
        slank_data = json.load(f)
    slank_dict = {item['slank'].lower(): item['slankmean'].lower() for item in slank_data}
    
    # Memuat daftar stopword
    with open(stopword_path, 'r', encoding='utf-8') as f:
        stopword_list = json.load(f)
    stopword_set = set(word.lower() for word in stopword_list)
    
    logger.info(f"✓ Kamus dimuat: {len(slank_dict)} kata slang, {len(stopword_set)} stopword")
    return slank_dict, stopword_set


# ============================================================================
# FUNGSI 5: PEMBERSIHAN TEKS (TEXT PREPROCESSING)
# ============================================================================
def text_preprocessing(text):
    """
    Membersihkan teks dari:
    - URL/link
    - Emoticon
    - Hashtag
    - Karakter khusus
    - Mengubah ke huruf kecil
    """
    # Hapus URL
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
    
    # Hapus emoticon
    emoticon_pattern = re.compile(r'(?::|;|=)(?:-)?(?:\)|\(|D|P|O)')
    text = emoticon_pattern.sub('', text)
    
    # Hapus hashtag
    text = re.sub(r'#\w+', '', text)
    
    # Ubah ke huruf kecil
    text = text.lower()
    
    # Hapus karakter selain huruf dan angka
    text = re.sub(r'[^a-z0-9\s]', '', text)
    
    # Hapus spasi berlebih
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text


# ============================================================================
# FUNGSI 6: MENGHAPUS KATA SLANG
# ============================================================================
def remove_slang(text, slank_dict):
    """
    Mengubah kata slang menjadi kata baku
    Contoh: "gue" menjadi "saya", "gak" menjadi "tidak"
    """
    words = text.split()
    mapped = [slank_dict.get(w.lower(), w) for w in words]
    return ' '.join(mapped)


# ============================================================================
# FUNGSI 7: MENGHAPUS STOPWORD
# ============================================================================
def remove_stopwords(text, stopword_set):
    """
    Menghapus kata-kata yang tidak penting (stopword)
    Contoh: "yang", "di", "ke", "dari", dll
    """
    words = text.split()
    filtered = [w for w in words if w.lower() not in stopword_set]
    return ' '.join(filtered)


# ============================================================================
# FUNGSI 8: MEMANGGIL API GATA FRAMEWORK UNTUK STEMMING
# ============================================================================
def send_to_gata_framework(text, technique='3', max_retries=3, retry_delay=0.1):
    """
    Memanggil API GataFramework untuk proses stemming
    (mengubah kata ke bentuk dasarnya)
    
    Contoh: "berlari" menjadi "lari", "membaca" menjadi "baca"
    """
    encoded_text = urllib.parse.quote_plus(text.strip())
    url = f"{GATA_API_URL}{technique}&textbefore={encoded_text}"
    
    for attempt in range(max_retries + 1):
        try:
            logger.info(f"Memanggil GataFramework API - Stemming (percobaan {attempt + 1}/{max_retries + 1})")
            with urllib.request.urlopen(url) as response:
                result = response.read().decode('utf-8')
                logger.info(f"✓ GataFramework API Berhasil - Stemming")
                time.sleep(0.03)
                return result
        except Exception as e:
            logger.warning(f"✗ GataFramework API Error - Stemming: {str(e)}")
            if attempt < max_retries:
                wait_time = retry_delay * (attempt + 1)
                logger.info(f"Mencoba lagi dalam {wait_time}s...")
                time.sleep(wait_time)
                continue
            logger.error(f"✗ GataFramework API Gagal setelah {max_retries + 1} percobaan - Stemming")
            return "time out"
    return "time out"


# ============================================================================
# FUNGSI 9: MEMPROSES SATU BARIS DATA
# ============================================================================
def process_single_row(row, slank_dict, stopword_set):
    """
    Memproses satu review melalui semua tahapan:
    1. Pembersihan teks
    2. Menghapus slang
    3. Menghapus stopword
    4. Stemming
    """
    row_num = row.get('no', 'Unknown')
    logger.debug(f"Memproses baris {row_num}")
    
    # Mulai dengan teks asli
    txt = text_preprocessing(row['ulasan'])
    result = row.copy()
    
    # Hapus slang
    txt = remove_slang(txt, slank_dict)
    result['slang'] = txt
    
    # Hapus stopword
    txt = remove_stopwords(txt, stopword_set)
    result['indonesian_stopword_removal'] = txt
    
    # Stemming menggunakan API
    txt = send_to_gata_framework(txt, '3')
    result['indonesian_stemming'] = txt
    
    logger.debug(f"✓ Baris {row_num} selesai")
    return result


# ============================================================================
# FUNGSI 10: MEMPROSES SEMUA DATA (TEXT MINING)
# ============================================================================
def process_text_mining(df, slank_dict, stopword_set, max_workers=4):
    """
    Memproses semua review secara paralel untuk mempercepat
    """
    total_rows = len(df)
    logger.info(f"Memulai text mining dengan {total_rows} baris menggunakan {max_workers} workers...")
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {
            executor.submit(process_single_row, row, slank_dict, stopword_set): idx 
            for idx, (_, row) in enumerate(df.iterrows())
        }
        results = []
        completed = 0
        for future in as_completed(futures):
            completed += 1
            result = future.result()
            results.append(result)
            logger.info(f"Progress: {completed}/{total_rows} ({(completed/total_rows)*100:.1f}%)")
    
    logger.info(f"✓ Text mining selesai! Total baris diproses: {total_rows}")
    return pd.DataFrame(results)


# ============================================================================
# FUNGSI 11: MENYIMPAN HASIL AKHIR
# ============================================================================
def export_results(processed_df, path='data/bank-permata-labeling-data-set-result.xlsx'):
    """
    Menyimpan hasil akhir ke file Excel
    """
    processed_df.to_excel(path, index=False)
    logger.info(f"✓ Hasil disimpan ke: {path}")


# ============================================================================
# FUNGSI UTAMA (MAIN)
# ============================================================================
def main():
    """
    Fungsi utama yang menjalankan semua proses secara berurutan
    """
    logger.info("=" * 80)
    logger.info("MEMULAI ANALISIS REVIEW PERMATA BANK")
    logger.info("=" * 80)
    
    try:
        # LANGKAH 1: Ambil review dari Play Store
        logger.info("\n[LANGKAH 1/6] Mengambil review dari Google Play Store...")
        raw_reviews = fetch_reviews_from_playstore()
        
        # LANGKAH 2: Siapkan data dalam bentuk tabel
        logger.info("\n[LANGKAH 2/6] Menyiapkan dataframe...")
        df = prepare_dataframe(raw_reviews)
        save_raw_data(df)
        
        # LANGKAH 3: Beri label otomatis
        logger.info("\n[LANGKAH 3/6] Memberikan label otomatis...")
        labeled_data = auto_label_data(df)
        save_labeled_data(labeled_data)
        
        # LANGKAH 4: Muat kamus slang dan stopword
        logger.info("\n[LANGKAH 4/6] Memuat kamus...")
        slank_dict, stopword_set = load_dictionaries()
        
        # LANGKAH 5: Proses text mining
        logger.info("\n[LANGKAH 5/6] Memproses text mining...")
        processed_df = process_text_mining(labeled_data, slank_dict, stopword_set, max_workers=4)
        
        # LANGKAH 6: Simpan hasil
        logger.info("\n[LANGKAH 6/6] Menyimpan hasil...")
        export_results(processed_df)
        
        logger.info("\n" + "=" * 80)
        logger.info("✓ PROSES SELESAI DENGAN SUKSES!")
        logger.info("=" * 80)
        
    except Exception as e:
        logger.error(f"✗ Proses gagal dengan error: {str(e)}", exc_info=True)
        raise


# ============================================================================
# MENJALANKAN PROGRAM
# ============================================================================
if __name__ == "__main__":
    main()