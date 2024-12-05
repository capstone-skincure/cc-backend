const newsModel = require('../models/news');

const getNews = async () => {
  try {
    const news = await newsModel.getAllNews();
    return news;
  } catch (error) {
    throw new Error(error.message);
  }
};

const createNews = async (newsData) => {
  try {
    await newsModel.addNews(newsData);
    return { message: 'News successfully added!' };
  } catch (error) {
    throw new Error('Failed to add news: ' + error.message);
  }
};

module.exports = {
  getNews,
  createNews,
};
