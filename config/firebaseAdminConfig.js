require('dotenv').config();
const admin = require('firebase-admin');

// Validasi environment variables
if (!process.env.FIREBASE_PROJECT_ID || !process.env.FIREBASE_PRIVATE_KEY || !process.env.FIREBASE_CLIENT_EMAIL) {
    console.error("Error: Firebase environment variables are not properly set.");
    process.exit(1); // Keluar jika ada variabel lingkungan yang tidak tersedia
}

// Inisialisasi Firebase Admin SDK
const adminApp = admin.initializeApp({
    credential: admin.credential.cert({
        projectId: process.env.FIREBASE_PROJECT_ID,
        privateKey: process.env.FIREBASE_PRIVATE_KEY.replace(/\\n/g, '\n'),
        clientEmail: process.env.FIREBASE_CLIENT_EMAIL,
    }),
});

console.log("Firebase Admin SDK initialized successfully.");

module.exports = adminApp;