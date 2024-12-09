import os
import io
import json
import tensorflow as tf
from flask import Flask, request, jsonify
from google.cloud import storage
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime
import random
from flask_cors import CORS

# Inisialisasi aplikasi Flask
app = Flask(__name__)

# Inisialisasi Firebase Admin SDK
cred = credentials.Certificate(r"C:\javascript-projects\skincure-flask\node-js-app\config\skincure-442717-firebase-adminsdk-d1trp-1ef62e74a2.json")
firebase_admin.initialize_app(cred)

# Inisialisasi Firestore
db = firestore.client()

# Set up Google Cloud Storage client
storage_client = storage.Client()

# Bucket dan file model
BUCKET_NAME = "skincure-bucket1"
MODEL_PATH = "model/model.h5"
LOCAL_MODEL_PATH = "local_model.h5"

# Fungsi untuk mengunduh model dari GCS
def download_model_from_gcs(bucket_name, model_path, local_path):
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(model_path)
    # Unduh model dari GCS dan simpan sebagai file lokal
    blob.download_to_filename(local_path)
    print(f"Model downloaded to {local_path}")

# Fungsi untuk memuat model ke memori dari file lokal
def load_model_from_gcs():
    # Download model terlebih dahulu ke path lokal
    download_model_from_gcs(BUCKET_NAME, MODEL_PATH, LOCAL_MODEL_PATH)
    
    # Muat model menggunakan TensorFlow
    model = tf.keras.models.load_model(LOCAL_MODEL_PATH)
    print("Model berhasil dimuat.")
    return model

# Muat model saat aplikasi Flask dimulai
model = load_model_from_gcs()

# Fungsi untuk memverifikasi token Firebase
def verify_firebase_token(id_token):
    try:
        # Verifikasi token Firebase
        decoded_token = auth.verify_id_token(id_token)
        uid = decoded_token['uid']
        return uid
    except Exception as e:
        print(f"Token verification failed: {str(e)}")
        return None
    
def get_description_by_condition(kondisi):
    try:
        descriptions_ref = db.collection("descriptions")
        query = descriptions_ref.where("kondisi", "==", kondisi)
        docs = list(query.stream())

        # Debugging: Log hasil query
        print(f"Querying Firestore for condition: {kondisi}")
        print(f"Documents found: {len(docs)}")

        if not docs:
            print(f"No matching documents found for condition: {kondisi}")
            return {
                "description": "Kulit Anda Sehat! Stay Healthy ya!",
                "kondisi": "Healthy Skin",
                "cara pencegahan": "No pencegahan available",
                "pengobatan": "No pengobatan available",
                "penjelasan": "No penjelasan available",
                "penyebab": "No penyebab available"
            }

        # Ambil data dari dokumen pertama
        data = docs[0].to_dict()

        # Debugging: Log data yang diambil dari Firestore
        print(f"Fetched description data: {data}")

        # Bentuk deskripsi dari data yang ada
        description = f"Kondisi: {kondisi}\n"
        description += f"Penyebab: {data.get('penyebab ', 'Tidak tersedia')}\n"
        description += f"Pencegahan: {data.get('cara pencegahan', 'Tidak tersedia')}\n"
        description += f"Pengobatan: {data.get('pengobatan', 'Tidak tersedia')}\n"
        description += f"Penjelasan: {data.get('penjelasan ', 'Tidak tersedia')}\n"

        return {
            "description": description,
            "kondisi": data.get("kondisi", kondisi),
            "pencegahan": data.get("cara pencegahan", "Tidak tersedia"),
            "pengobatan": data.get("pengobatan", "Tidak tersedia"),
            "penjelasan": data.get("penjelasan ", "Tidak tersedia"),
            "penyebab": data.get("penyebab ", "Tidak tersedia")
        }
    except Exception as e:
        print(f"Error fetching description: {str(e)}")
        return {
            "description": "An error occurred while fetching description.",
            "kondisi": kondisi,
            "pencegahan": "No pencegahan available",
            "pengobatan": "No pengobatan available",
            "penjelasan": "No penjelasan available",
            "penyebab": "No penyebab available"
        }

def save_prediction_to_firestore(result):
    description_data = get_description_by_condition(result)  # Ambil data deskripsi

    prediction_id = str(random.randint(100000, 999999))  # Buat ID unik untuk prediksi
    prediction_ref = db.collection("predictions").document(prediction_id)

    prediction_data = {
        "createdAt": datetime.now().isoformat(),
        "description": description_data["description"],  # Gunakan deskripsi yang dibentuk
        "id": prediction_id,
        "result": result,
        "status_code": 200
    }

    # Debugging
    print(f"Saving prediction: {prediction_data}")

    prediction_ref.set(prediction_data)
    print(f"Hasil prediksi disimpan dengan ID: {prediction_id}")

    return prediction_id

# Endpoint untuk menerima gambar dan melakukan prediksi
@app.route("/predict", methods=["POST"])
def predict():
    # Ambil token Firebase dari header Authorization
    id_token = request.headers.get("Authorization")

    if not id_token:
        return jsonify({"error": "Authorization token missing"}), 400

    # Verifikasi token
    uid = verify_firebase_token(id_token)
    if not uid:
        return jsonify({"error": "Invalid or expired token"}), 401
    
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files["file"]

    # Validasi tipe file
    if file.filename == "" or not file.content_type.startswith("image/"):
        return jsonify({"error": "Invalid file type, only image files are allowed"}), 400
    
    try:
        # Baca gambar
        img = tf.image.decode_image(file.read(), channels=3)
        img = tf.image.resize(img, (224, 224))  # Sesuaikan ukuran dengan input model
        img = tf.expand_dims(img, axis=0)  # Batch size 1

        # Prediksi
        predictions = model.predict(img)
        predicted_class = tf.argmax(predictions, axis=1).numpy()[0]
        class_names = ['Acne', 'Carcinoma', 'Eczema', 'Keratosis', 'Milia', 'Rosacea']  # Sesuaikan dengan kelas yang Anda miliki
        
        result = class_names[predicted_class]

        # Simpan hasil prediksi ke Firestore dan ambil prediction_id
        prediction_id = save_prediction_to_firestore(result)
        
        # Ambil deskripsi dari kondisi yang diprediksi
        description = get_description_by_condition(result)
        
        return jsonify({
            "status_code": 200,
            "createdAt": datetime.now().isoformat(),
            "description": description["description"],
            "id": prediction_id,
            "result": result
        }), 200
    
    except Exception as e:
        return jsonify({"status_code": 500, "error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
