const express = require('express');
const dotenv = require('dotenv');
const newsRoutes = require('./src/routes/newsRoutes');
const handleError = require('./src/utils/errorHandler');

dotenv.config();

const app = express();
const PORT = process.env.PORT || 5000;

app.use(express.json());

app.use('/api/news', newsRoutes);

// Error handling middleware
app.use((err, req, res, next) => {
  handleError(err, res);
});

app.listen(PORT, () => {
  console.log(`Server running on http://localhost:${PORT}`);
});
