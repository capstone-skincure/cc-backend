const admin = require('../config/firebaseConfig');

const getAllNews = async () => {
  const newsRef = admin.firestore().collection('NEWS');
  const snapshot = await newsRef.get();
  
  if (snapshot.empty) {
    throw new Error('No news available');
  }

  const newsData = snapshot.docs.map(doc => doc.data());
  return newsData;
};

const addNews = async (news) => {
  const newsRef = admin.firestore().collection('NEWS');
  await newsRef.add(news);
  return { message: 'News added successfully!' };
};

module.exports = {
  getAllNews,
  addNews,
};
