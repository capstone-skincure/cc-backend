// /express-api/services/contactusService.js
const { createContactusInFirestore, getAllContactusFromFirestore } = require('../models/contactusModel');

const createContactus = async (contactData) => {
  return await createContactusInFirestore(contactData);
};

const getAllContactus = async () => {
  return await getAllContactusFromFirestore();
};

module.exports = { createContactus, getAllContactus };
