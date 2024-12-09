const express = require('express');
const dotenv = require('dotenv');
const newsRoutes = require('./routes/newsRoutes');
const contactusRoutes = require('./routes/contactusRoutes');
const authRoutes = require('./routes/authRoutes');
const handleError = require('./utils/errorHandler');
const fileUpload = require('express-fileupload');
const axios = require('axios');
const FormData = require('form-data');

dotenv.config();

const app = express();
const PORT = process.env.PORT || 8001;

// Middleware
app.use(express.json());
app.use(express.urlencoded({ extended: true })); // Untuk menangani form-data jika perlu
app.use(fileUpload()); // Middleware untuk file upload

// Routes
app.use('/api/news', newsRoutes);
app.use('/api/contactus', contactusRoutes);
app.use('/api/auth', authRoutes);

// Route baru untuk menerima gambar dan mengirimkannya ke Flask
app.post('/api/predict', async (req, res) => {
  console.log('Request received at /api/predict');
  try {
    // Validasi keberadaan file
    if (!req.files || !req.files.file) {
      console.error('No file provided.');
      return res.status(400).json({ message: 'No file provided.' });
    }

    const file = req.files.file;
    console.log('File received:', file.name);

    // Ambil token dari header
    const tokenValue = req.headers['authorization']?.split(' ')[1]; // Mengambil token Bearer

    if (!tokenValue) {
      console.error('No token provided.');
      return res.status(400).json({ message: 'No token provided.' });
    }

    // Kirim file ke Flask
    const formData = new FormData();
    formData.append('file', file.data, file.name);

    console.log('Sending request to Flask...');
    const response = await axios.post('http://127.0.0.1:8000/predict', formData, {
      headers: {
        'Authorization': `Bearer ${tokenValue}`,
        ...formData.getHeaders(),
      }
    });
    console.log('Response from Flask:', response.data);

    // Kirimkan hasil prediksi yang diterima dari Flask ke client
    return res.status(200).json(response.data);
  } catch (error) {
    // Error handling
    if (error.response) {
      console.error('Flask error:', error.response.data);
      return res.status(500).json({ message: 'Error from Flask', details: error.response.data });
    } else if (error.request) {
      console.error('No response from Flask:', error.request);
      return res.status(500).json({ message: 'No response from Flask' });
    } else {
      console.error('Error during prediction:', error.message);
      return res.status(500).json({ message: 'Internal server error.', details: error.message });
    }
  }
});

// Error handling middleware
app.use((err, req, res, next) => {
  handleError(err, res);
});

// Start server
app.listen(PORT, () => {
  console.log(`Server running on http://localhost:${PORT}`);
});
