const { getAllNewsFromFirestore } = require('../models/newsModel');

// Controller untuk mengambil semua berita
const getAllNews = async (req, res) => {
  try {
    const news = await getAllNewsFromFirestore();
    res.status(200).json(news);
  } catch (error) {
    res.status(500).json({
      message: 'Error retrieving news',
      error: error.message,
    });
  }
};

module.exports = { getAllNews };
