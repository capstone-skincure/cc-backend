const { body, validationResult } = require('express-validator');
const { check, validationResult } = require('express-validator');

// Validator for news creation
const validateNewsInput = [
  body('name').notEmpty().withMessage('Name is required'),
  body('description').notEmpty().withMessage('Description is required'),
  body('image').notEmpty().withMessage('Image URL is required'),
];

// Validator for user authentication (for example, login)
const validateAuthInput = [
  body('email').isEmail().withMessage('Invalid email format'),
  body('password').isLength({ min: 6 }).withMessage('Password should be at least 6 characters'),
];

// Middleware to handle validation errors
const validateRequest = (req, res, next) => {
  const errors = validationResult(req);
  if (!errors.isEmpty()) {
    return res.status(400).json({ errors: errors.array() });
  }
  next();
};

// Validator untuk body request
const validateContactusData = [
  check('name').notEmpty().withMessage('Name is required'),
  check('description').notEmpty().withMessage('Description is required'),
  check('image').notEmpty().withMessage('Image URL is required'),
];

module.exports = {
  validateNewsInput,
  validateAuthInput,
  validateRequest,
  validateContactusData,
};
