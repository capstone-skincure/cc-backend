const admin = require('../config/firebaseAdminConfig');
const db = admin.firestore();

// Fungsi untuk mengambil berita dari Firestore
const getAllNewsFromFirestore = async () => {
  const newsSnapshot = await db.collection('news')
    .orderBy('createdAt', 'desc')
    .limit(10)
    .get();

  const newsList = [];
  newsSnapshot.forEach(doc => {
    newsList.push({ id: doc.id, ...doc.data() });
  });

  return newsList;
};

module.exports = { getAllNewsFromFirestore };
