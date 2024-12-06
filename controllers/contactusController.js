// /express-api/controllers/contactusController.js
const { createContactusInFirestore, getAllContactusFromFirestore } = require('../models/contactusModel');

// Controller untuk membuat contactus baru
const createContactus = async (req, res) => {
  try {
    const { name, description, image } = req.body;
    const contactId = await createContactusInFirestore({ name, description, image });
    res.status(201).json({ message: 'Contactus entry created successfully', contactId });
  } catch (error) {
    res.status(500).json({ message: 'Error creating contactus entry', error: error.message });
  }
};

// Controller untuk mengambil semua contactus
const getAllContactus = async (req, res) => {
  try {
    const contactus = await getAllContactusFromFirestore();
    res.status(200).json(contactus);
  } catch (error) {
    res.status(500).json({ message: 'Error retrieving contactus data', error: error.message });
  }
};

module.exports = { createContactus, getAllContactus };
