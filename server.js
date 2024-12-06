const express = require('express');
const dotenv = require('dotenv');
const newsRoutes = require('./src/routes/newsRoutes');
const handleError = require('./src/utils/errorHandler');
const contactusRoutes = require('./routes/contactusRoutes'); 

dotenv.config();

const app = express();
const PORT = process.env.PORT || 8000;

app.use(express.json());

app.use('/api/news', newsRoutes);
app.use('/api/auth', authRoutes);
app.use('/api/contactus', contactusRoutes);

// Error handling middleware
app.use((err, req, res, next) => {
  handleError(err, res);
});

app.listen(PORT, () => {
  console.log(`Server running on http://localhost:${PORT}`);
});
