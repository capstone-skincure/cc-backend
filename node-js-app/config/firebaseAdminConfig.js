require('dotenv').config();
const admin = require('firebase-admin');

// Validasi environment variables
if (!process.env.FIREBASE_PROJECT_ID || !process.env.FIREBASE_PRIVATE_KEY || !process.env.FIREBASE_CLIENT_EMAIL) {
    console.error("Error: Firebase environment variables are not properly set.");
    process.exit(1);
}

// Inisialisasi Firebase Admin SDK hanya jika belum ada aplikasi yang diinisialisasi
if (admin.apps.length === 0) {
    admin.initializeApp({
        credential: admin.credential.cert({
            projectId: process.env.FIREBASE_PROJECT_ID,
            privateKey: process.env.FIREBASE_PRIVATE_KEY.replace(/\\n/g, '\n'),
            clientEmail: process.env.FIREBASE_CLIENT_EMAIL,
        }),
    });
    console.log("Firebase Admin SDK initialized successfully.");
} else {
    console.log("Firebase Admin SDK already initialized.");
}

module.exports = admin;
