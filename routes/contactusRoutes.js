const express = require('express');
const { validateContactusData, validateRequest } = require('../validators/inputValidator');
const { createContactus } = require('../controllers/contactusController');
const verifyToken = require('../middlewares/authMiddleware'); // Mengimpor authMiddleware

const router = express.Router();

// Route untuk membuat contactus baru (hanya bisa diakses oleh pengguna yang sudah login)
router.post('/', verifyToken, validateContactusData, validateRequest, createContactus);

module.exports = router;
