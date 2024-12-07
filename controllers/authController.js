const admin = require('../config/firebaseConfig');

// Handle user registration (create new user)
const registerUser = async (req, res) => {
  const { email, password } = req.body;
  try {
    const userRecord = await admin.auth().createUser({
      email,
      password,
    });
    const token = await admin.auth().createCustomToken(userRecord.uid);
    res.status(201).json({
      message: 'Registration successful',
      token,
    });
  } catch (error) {
    res.status(500).json({
      message: 'Error registering user: ' + error.message,
    });
  }
};

// Handle user login (email and password validation)
const loginUser = async (req, res) => {
  const { email, password } = req.body;
  try {
    const userCredential = await admin.auth().getUserByEmail(email);
    const token = await admin.auth().createCustomToken(userCredential.uid);
    res.status(200).json({
      message: 'Login successful',
      token,
    });
  } catch (error) {
    if (error.code === 'auth/user-not-found') {
      return res.status(404).json({
        message: 'User not found',
      });
    }
    res.status(500).json({
      message: 'Error logging in: ' + error.message,
    });
  }
};

// Verify Firebase token and user ID
const verifyToken = async (req, res, next) => {
  const token = req.headers['authorization']?.split('Bearer ')[1];
  const userId = req.headers['userid'];
  if (!token || !userId) {
    return res.status(400).json({ message: 'Bad Request: Missing token or user ID' });
  }
  try {
    const decodedToken = await admin.auth().verifyIdToken(token);
    if (decodedToken.uid !== userId) {
      return res.status(401).json({ message: 'Unauthorized: Invalid user ID' });
    }
    req.user = decodedToken;
    next();
  } catch (error) {
    return res.status(401).json({ message: 'Unauthorized: Invalid or expired token' });
  }
};

module.exports = {
  registerUser,
  loginUser,
  verifyToken,
};
