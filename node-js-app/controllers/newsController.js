const { getAllNewsFromFirestore } = require('../models/newsModel');

// Controller untuk mengambil semua berita
const getAllNews = async (req, res) => {
  try {
    const news = await getAllNewsFromFirestore();  // Mengambil data berita menggunakan model
    res.status(200).json(news);  // Mengirimkan berita sebagai response
  } catch (error) {
    res.status(500).json({
      message: 'Error retrieving news',
      error: error.message,
    });
  }
};

module.exports = { getAllNews };
