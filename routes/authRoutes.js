const express = require('express');
const { validateAuthInput, validateRequest } = require('../validators/inputValidator');
const authController = require('../controllers/authController');

const router = express.Router();

// Route for logging in users
router.post('/login', validateAuthInput, validateRequest, authController.loginUser);

module.exports = router;
