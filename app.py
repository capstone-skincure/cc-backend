from flask import Flask, request, jsonify
import tensorflow as tf
import numpy as np

app = Flask(__name__)
model = tf.keras.models.load_model('path/to/your/model')

@app.route('/predict', methods=['POST'])
def predict():
    file = request.files['file']
    img = tf.io.decode_image(file.read(), channels=3)
    img = tf.image.resize(img, (224, 224))  
    img = tf.expand_dims(img, axis=0) / 255.0
    predictions = model.predict(img)
    return jsonify({'predictions': predictions.tolist()})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)