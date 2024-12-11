const admin = require('../config/firebaseAdminConfig');

const authMiddleware = async (req, res, next) => {
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
    return res.status(401).json({
      message: 'Unauthorized: Invalid or expired token',
      error: error.message
    });
  }
};

module.exports = authMiddleware;
