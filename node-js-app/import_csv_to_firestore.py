import pandas as pd
from google.cloud import firestore

# Fungsi untuk menambah data CSV ke Firestore
def add_csv_to_firestore(csv_file_path, collection_name):
    # Membaca CSV dengan encoding yang berbeda
    df = pd.read_csv(csv_file_path, encoding='latin1')  # Coba dengan 'latin1' atau 'ISO-8859-1'
    
    # Menyambungkan ke Firestore
    db = firestore.Client()
    
    # Looping melalui setiap baris di CSV
    for index, row in df.iterrows():
        doc_ref = db.collection(collection_name).document()  # Membuat document baru
        doc_ref.set(row.to_dict())  # Menyimpan baris sebagai dictionary
    
    print(f"Data CSV berhasil ditambahkan ke koleksi {collection_name}.")

# Panggil fungsi untuk menambah data dari CSV
add_csv_to_firestore('skin_description.csv', 'descriptions')  # Ganti path ke file CSV Anda
