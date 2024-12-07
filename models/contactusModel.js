const admin = require('../config/firebaseConfig');

// Menyimpan data contactus ke Firestore
const createContactusInFirestore = async ({ name, email, message, userId }) => {
  try {
    const contactRef = admin.firestore().collection('contactus');
    const docRef = await contactRef.add({
      name,
      email,
      message,
      userId, // Menyimpan userId yang didapatkan dari Firebase authentication
      createdAt: admin.firestore.FieldValue.serverTimestamp(),
    });
    return docRef.id; // Mengembalikan ID dari entry yang baru dibuat
  } catch (error) {
    throw new Error('Error saving contactus data: ' + error.message);
  }
};

module.exports = { createContactusInFirestore };
