import os
import io
import json
import tensorflow as tf
from flask import Flask, request, jsonify
from google.cloud import storage
import firebase_admin
from firebase_admin import credentials, firestore, auth
from datetime import datetime
import random
from flask_cors import CORS
import jwt
from urllib.parse import quote

# Inisialisasi aplikasi Flask
app = Flask(__name__)

# Mengizinkan CORS pada Flask
CORS(app)

# Inisialisasi Firebase Admin SDK
cred = credentials.Certificate("config/skincure-442717-firebase-adminsdk-d1trp-1ef62e74a2.json")
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
    
    blob.download_to_filename(local_path)
    print(f"Model downloaded to {local_path}")

# Fungsi untuk memuat model ke memori dari file lokal
def load_model_from_gcs():
    download_model_from_gcs(BUCKET_NAME, MODEL_PATH, LOCAL_MODEL_PATH)
    try:
        model = tf.keras.models.load_model(LOCAL_MODEL_PATH, compile=False)
        print("Model berhasil dimuat.")
        return model
    except Exception as e:
        print(f"Error loading model: {str(e)}")
        raise e

# Muat model saat aplikasi Flask dimulai
model = load_model_from_gcs()

# Fungsi untuk memverifikasi token Firebase
def verify_firebase_token(id_token):
    try:
        decoded_token = auth.verify_id_token(id_token)
        print(f"Decoded token: {decoded_token}")
        return decoded_token['uid']
    except auth.InvalidIdTokenError as e:
        print(f"Invalid token: {str(e)}")
    except auth.ExpiredIdTokenError as e:
        print(f"Expired token: {str(e)}")
    except Exception as e:
        print(f"Token verification failed: {str(e)}")
    return None
    
def get_description_by_condition(kondisi):
    try:
        descriptions_ref = db.collection("descriptions")
        query = descriptions_ref.where("kondisi", "==", kondisi)
        docs = list(query.stream())

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

        data = docs[0].to_dict()
        print(f"Fetched description data: {data}")

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
    
def upload_image_to_gcs(bucket_name, file, filename):
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(filename)

    file.stream.seek(0)
    blob.upload_from_file(file.stream, content_type=file.content_type)

    blob.make_public()
    return blob.public_url
    
def save_prediction_to_firestore(result, uid, confidence_score, image_url):
    description_data = get_description_by_condition(result)
    prediction_id = str(random.randint(100000, 999999))
    user_ref = db.collection("users").document(uid).collection("predictions").document(prediction_id)

    prediction_data = {
        "createdAt": datetime.now().isoformat(),
        "description": description_data["description"],
        "id": prediction_id,
        "result": result,
        "confidence_score": confidence_score * 100,
        "status_code": 200,
        "image_url": image_url
    }

    user_ref.set(prediction_data)
    print(f"Hasil prediksi disimpan untuk pengguna {uid} dengan ID prediksi: {prediction_id}")

    return prediction_id

# Endpoint untuk menerima gambar dan melakukan prediksi
@app.route("/predict", methods=["POST"])
def predict():
    id_token = request.headers.get("Authorization")
    if not id_token:
        return jsonify({"error": "Authorization token missing"}), 400

    if id_token.startswith("Bearer "):
        id_token = id_token.split("Bearer ")[1]

    uid = verify_firebase_token(id_token)
    if not uid:
        return jsonify({"error": "Invalid or expired token"}), 401
    
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files["file"]
    try:
        filename = f"{uid}_{datetime.now().strftime('%Y%m%d%H%M%S')}.jpg"
        image_url = upload_image_to_gcs(BUCKET_NAME, file, filename)

        file.stream.seek(0)
        img = tf.image.decode_image(file.read(), channels=3)
        img = tf.image.resize(img, (224, 224))
        img = tf.expand_dims(img, axis=0)

        predictions = model.predict(img)
        predicted_class = int(tf.argmax(predictions, axis=1).numpy()[0])
        class_names = ['Acne', 'Carcinoma', 'Eczema', 'Keratosis', 'Milia', 'Rosacea']
        
        result = class_names[predicted_class]
        confidence_score = float(predictions[0][predicted_class])
        
        prediction_id = save_prediction_to_firestore(result, uid, confidence_score, image_url)

        user_ref = db.collection("users").document(uid).collection("predictions").document(prediction_id)
        user_ref.update({"image_url": image_url})

        description = get_description_by_condition(result)
        
        return jsonify({
            "status_code": 200,
            "createdAt": datetime.now().isoformat(),
            "description": description["description"],
            "id": prediction_id,
            "result": result,
            "confidence_score": confidence_score * 100,
            "image_url": image_url
            
        }), 200
    
    except Exception as e:
        return jsonify({"status_code": 500, "error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))  # Gunakan PORT dari environment
    app.run(host="0.0.0.0", port=port)