const express = require('express');
const dotenv = require('dotenv');
const newsRoutes = require('./routes/newsRoutes');
const handleError = require('./utils/errorHandler');
const contactusRoutes = require('./routes/contactusRoutes');
const admin = require('./config/firebaseAdminConfig');
const authRoutes = require('./routes/authRoutes');
const axios = require('axios');

dotenv.config();

const app = express();
const PORT = process.env.PORT || 8001;

app.use(express.json());
app.use(express.urlencoded({ extended: true })); // Untuk menangani form-data jika perlu

app.use('/api/news', newsRoutes);
app.use('/api/contactus', contactusRoutes);
app.use('/api/auth', authRoutes);

// Route baru untuk menerima gambar dan mengirimkannya ke Flask
app.post('/api/predict', async (req, res) => {
  try {
    if (!req.files || !req.files.image) {
      return res.status(400).json({ message: 'No image file provided.' });
    }

    const image = req.files.image;

    // Kirim gambar ke Flask (misalnya ke endpoint /predict Flask)
    const formData = new FormData();
    formData.append('file', image.data, image.name);

    const response = await axios.post('http://localhost:8000/predict', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });

    // Kirimkan hasil prediksi yang diterima dari Flask ke client
    return res.status(200).json(response.data);
  } catch (error) {
    console.error('Error during prediction:', error);
    return res.status(500).json({ message: 'Internal server error.' });
  }
});

app.use((err, req, res, next) => {
  handleError(err, res);
});

app.listen(PORT, () => {
  console.log(`Server running on http://localhost:${PORT}`);
});
