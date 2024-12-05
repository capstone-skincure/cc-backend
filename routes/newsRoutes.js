const express = require('express');
const authMiddleware = require('../middlewares/authMiddleware');
const newsController = require('../controllers/newsController');

const router = express.Router();

router.get('/get', authMiddleware, newsController.getNews);
router.post('/create', authMiddleware, newsController.createNews);

module.exports = router;
