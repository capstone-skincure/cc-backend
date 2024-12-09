const express = require('express');
const admin = require('../config/firebaseAdminConfig');
const { validateAuthInput, validateRequest } = require('../validators/inputValidator');
const authController = require('../controllers/authController');

const router = express.Router();

// Route for logging in users
router.post('/login', validateAuthInput, validateRequest, authController.loginUser);
router.post('/register', validateAuthInput, validateRequest, authController.registerUser);

module.exports = router;
