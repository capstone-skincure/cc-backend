const express = require('express');
const dotenv = require('dotenv');
const newsRoutes = require('./routes/newsRoutes');
const handleError = require('./utils/errorHandler');
const contactusRoutes = require('./routes/contactusRoutes'); 
const admin = require('./config/firebaseAdminConfig');
const authRoutes = require('./routes/authRoutes');

dotenv.config();

const app = express();
const PORT = process.env.PORT || 8000;

app.use(express.json());

app.use('/api/news', newsRoutes);
app.use('/api/contactus', contactusRoutes);
app.use('/api/auth', authRoutes);

// Error handling middleware
app.use((err, req, res, next) => {
  handleError(err, res);
});

app.listen(PORT, () => {
  console.log(`Server running on http://localhost:${PORT}`);
});
