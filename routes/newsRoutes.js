const express = require('express');
const { getAllNews } = require('../controllers/newsController');

const router = express.Router();

// Route untuk mengambil semua berita
router.get('/', getAllNews);

module.exports = router;
