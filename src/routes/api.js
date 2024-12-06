const express = require('express');
const multer = require('multer');
const { analyzeImage } = require('../services/model');
const { uploadImageToCloudStorage } = require('../services/storage');
const admin = require('../config/firebase');

const router = express.Router();
const upload = multer({ dest: 'uploads/' }); 

async function authenticate(req, res, next) {
    const token = req.headers.authorization?.split(' ')[1];
    if (!token) {
        return res.status(401).json({ message: 'Unauthorized' });
    }
    try {
        const decodedToken = await admin.auth().verifyIdToken(token);
        req.user = decodedToken;
        next();
    } catch (error) {
        return res.status(403).json({ message: 'Forbidden' });
    }
}

router.use(authenticate);

router.post('/analyze', upload.single('image'), async (req, res) => {
    try {
        const imageUrl = await uploadImageToCloudStorage(req.file);

        const analysisResult = await analyzeImage(imageUrl);

        res.json({
            success: true,
            data: analysisResult,
        });
    } catch (error) {
        console.error(error);
        res.status(500).json({ success: false, message: 'Server error' });
    }
});

module.exports = router;
