// /express-api/routes/contactusRoutes.js
const express = require('express');
const router = express.Router();
const { createContactus, getAllContactus } = require('../controllers/contactusController');

// Route untuk mendapatkan semua contactus
router.get('/', getAllContactus);

// Route untuk membuat contactus baru
router.post('/', createContactus);

module.exports = router;
