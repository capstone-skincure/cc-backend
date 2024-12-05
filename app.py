import os
import base64
import io
import numpy as np
import cv2
import tensorflow as tf
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from google.cloud import storage, firestore
from tensorflow.keras.utils import get_custom_objects
from tensorflow.keras.models import load_model
from model import CustomCNN

import pandas as pd

# Jumlah kelas sesuai kondisi kulit
num_classes = 6  # Sesuaikan dengan jumlah kelas yang kamu miliki

# Initialize the app
app = FastAPI()

# Set up Google Cloud client
storage_client = storage.Client()
firestore_client = firestore.Client()

# Define paths
bucket_name = "skincure-bucket1"
model_path = "modelh5/cnn_model.h5"
local_model_path = 'cnn_model.h5'

# Registrasi layer CustomCNN
get_custom_objects()['CustomCNN'] = CustomCNN

# Fungsi untuk mendownload model dari GCS
def download_blob(bucket_name, source_blob_name, local_model_path):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(source_blob_name)
    blob.download_to_filename(destination_file_name)
    print(f"Downloaded {source_blob_name} to {destination_file_name}.")

if not os.path.exists(local_model_path):
    print("Model file not found locally. Downloading from GCS...")
    download_blob(bucket_name, source_blob_name, destination_file_name)
else:
    print("Model file found locally.")
    
# Fungsi untuk memuat model dari GCS
def load_model_from_gcs(bucket_name, model_path):
    download_blob(bucket_name, model_path, local_model_path)

    # Pastikan model berhasil diunduh sebelum diload
    if not os.path.exists(local_model_path):
        raise FileNotFoundError(f"Model file {local_model_path} not found after downloading.")
    
    model = load_model(local_model_path, custom_objects={'CustomCNN': CustomCNN})
    return model

# Load the model (only once)
model = load_model_from_gcs(bucket_name, model_path)
print(f"Model input shape: {model.input_shape}")

# Class to accept input image
class ImageData(BaseModel):
    image: str  # Base64 encoded image string

# Dictionary for disease information
skin_descript = pd.DataFrame({
    'kondisi': ['Acne', 'Carcinoma', 'Eczema', 'Keratosis', 'Milia', 'Rosacea'],
    'penjelasan': ['Acne description', 'Carcinoma description', 'Eczema description', 
                   'Keratosis description', 'Milia description', 'Rosacea description'],
    'penyebab': ['Acne causes', 'Carcinoma causes', 'Eczema causes', 
                 'Keratosis causes', 'Milia causes', 'Rosacea causes'],
    'pengobatan': ['Acne treatment', 'Carcinoma treatment', 'Eczema treatment', 
                   'Keratosis treatment', 'Milia treatment', 'Rosacea treatment'],
    'pencegahan': ['Acne prevention', 'Carcinoma prevention', 'Eczema prevention', 
                   'Keratosis prevention', 'Milia prevention', 'Rosacea prevention']
})

disease_info = {
    row['kondisi']: {
        "penjelasan": row['penjelasan'],
        "penyebab": row['penyebab'],
        "pengobatan": row['pengobatan'],
        "pencegahan": row['pencegahan']
    }
    for _, row in skin_descript.iterrows()
}

# Class names for your model
class_names = ['Acne', 'Carcinoma', 'Eczema', 'Keratosis', 'Milia', 'Rosacea']

# Route to predict
@app.post("/predict/")
async def predict(data: ImageData):
    try:
        # Decode the image from base64
        image_data = base64.b64decode(data.image)
        np_arr = np.frombuffer(image_data, np.uint8)
        img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        # Validate input shape
        if img is None:
            raise ValueError("Invalid image data")
        if len(model.input_shape) != 4 or model.input_shape[1:] != (224, 224, 3):  # Sesuaikan ukuran input model
            raise ValueError("Model input shape is not valid for this image")

        # Preprocess the image
        img = cv2.resize(img, (224, 224))  # Ganti ukuran (224, 224) sesuai model input
        img = np.expand_dims(img, axis=0)  # Add batch dimension
        img = img / 255.0  # Normalize the image

        # Predict using the model
        predictions = model.predict(img)
        predicted_class = np.argmax(predictions, axis=1)

        # Get result class and description
        result = class_names[predicted_class[0]]
        description = disease_info[result]

        # Save the result in Firestore
        firestore_client.collection('predictions').add({
            'result': result,
            'description': description,
            'createdAt': firestore.SERVER_TIMESTAMP
        })

        # Return prediction result with description
        return JSONResponse(content={"result": result, "description": description})

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing the image: {str(e)}")

# Route to get the prediction history
@app.get("/predict/history/")
async def get_prediction_history():
    predictions_ref = firestore_client.collection('predictions')
    predictions = predictions_ref.stream()

    history = []
    for prediction in predictions:
        prediction_data = prediction.to_dict()
        history.append({
            "id": prediction.id,
            "result": prediction_data.get("result"),
            "description": prediction_data.get("description"),
            "createdAt": prediction_data.get("createdAt")
        })

    return JSONResponse(content={"status": "success", "data": history})

# Optional: Health check endpoint
@app.get("/health/")
async def health_check():
    return {"status": "OK"}

# Main entry point to run the app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
