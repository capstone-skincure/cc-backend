const { createContactusInFirestore } = require('../models/contactusModel');

// Controller untuk membuat contactus baru
const createContactus = async (req, res) => {
  try {
    const { name, email, message } = req.body;

    // Mendapatkan userId dari token yang sudah diverifikasi di middleware
    const userId = req.user.uid;

    // Validasi input
    if (!name || !email || !message) {
      return res.status(400).json({ message: 'All fields are required' });
    }

    // Menyimpan data contactus ke Firestore dengan userId
    const contactId = await createContactusInFirestore({ name, email, message, userId });

    res.status(201).json({
      message: 'Contactus entry created successfully',
      contactId,
    });
  } catch (error) {
    res.status(500).json({
      message: 'Error creating contactus entry',
      error: error.message,
    });
  }
};

module.exports = { createContactus };
