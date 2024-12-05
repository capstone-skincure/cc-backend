const newsService = require('../services/newsService');

const getNews = async (req, res) => {
  try {
    const news = await newsService.getNews();
    return res.status(200).json(news);
  } catch (error) {
    return res.status(500).json({ message: error.message });
  }
};

const createNews = async (req, res) => {
  const { name, description, image } = req.body;
  
  if (!name || !description || !image) {
    return res.status(400).json({ message: 'Bad Request: Missing required fields' });
  }

  try {
    const newsData = { name, description, image };
    const response = await newsService.createNews(newsData);
    return res.status(201).json(response);
  } catch (error) {
    return res.status(500).json({ message: error.message });
  }
};

module.exports = {
  getNews,
  createNews,
};
