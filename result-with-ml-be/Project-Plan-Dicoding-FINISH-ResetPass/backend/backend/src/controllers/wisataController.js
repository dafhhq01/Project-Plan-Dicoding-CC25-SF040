const fs = require('fs');
const path = require('path');
const csv = require('csv-parser');

const getWisataFromCSV = (req, res) => {
    const results = [];
    const filePath = path.join(__dirname, '../../machine-learning/data-wisata/data_wisata_cleaned.csv');

    fs.createReadStream(filePath)
        .pipe(csv({ separator: ',' }))
        .on('data', (data) => results.push(data))
        .on('end', () => {
            res.json(results);
        });
};

module.exports = { getWisataFromCSV };
