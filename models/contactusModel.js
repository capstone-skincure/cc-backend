// /express-api/models/contactusModel.js
const admin = require('firebase-admin');
const { FIREBASE_SERVICE_ACCOUNT } = process.env;

// Inisialisasi Firebase Admin SDK
admin.initializeApp({
  credential: admin.credential.cert(require(FIREBASE_SERVICE_ACCOUNT)),
  databaseURL: "https://your-project-id.firebaseio.com",
});

const db = admin.firestore();

// Model untuk membuat contactus di Firestore
const createContactusInFirestore = async (contactData) => {
  try {
    const contactRef = db.collection('contactus');
    const docRef = await contactRef.add({
      name: contactData.name,
      description: contactData.description,
      image: contactData.image,
      created_at: admin.firestore.FieldValue.serverTimestamp(),
    });
    return docRef.id;  // Kembalikan ID dokumen yang baru dibuat
  } catch (error) {
    throw new Error('Error creating contactus entry in Firestore');
  }
};

// Model untuk mengambil data contactus dari Firestore
const getAllContactusFromFirestore = async () => {
  try {
    const snapshot = await db.collection('contactus').get();
    const contactusList = snapshot.docs.map(doc => ({
      id: doc.id,
      ...doc.data(),
    }));
    return contactusList;
  } catch (error) {
    throw new Error('Error retrieving contactus data from Firestore');
  }
};

module.exports = { createContactusInFirestore, getAllContactusFromFirestore };
