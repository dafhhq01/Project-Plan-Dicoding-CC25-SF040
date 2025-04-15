const express = require('express');
const { getWisataFromCSV } = require('../controllers/wisataController');

const router = express.Router();
router.get('/wisata', getWisataFromCSV);

module.exports = router;
