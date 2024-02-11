const express = require('express');
const csv = require('csv-parser');
const fs = require('fs');
const multer = require('multer');
const { createWorker } = require('tesseract.js');

const app = express();

// Middleware to parse JSON
app.use(express.json());

// Setup multer for handling file uploads
const storage = multer.memoryStorage();
const upload = multer({ storage: storage });

// Endpoint to handle ingredient lookup
app.get('/ingredients/:name', (req, res) => {
    const ingredientName = req.params.name;
    const results = [];

    fs.createReadStream('ingredients.csv')
        .pipe(csv())
        .on('data', (data) => {
            if (data.name === ingredientName) {
                results.push({
                    source: data.source,
                    nature: data.nature
                });
            }
        })
        .on('end', () => {
            if (results.length > 0) {
                res.json(results);
            } else {
                res.status(404).json({ message: 'Ingredient not found' });
            }
        });
});

// Endpoint to handle image OCR and ingredient lookup
app.post('/scan', upload.single('image'), async (req, res) => {
    try {
        if (!req.file) {
            return res.status(400).json({ message: 'No image uploaded' });
        }

        // Perform OCR on the uploaded image
        const worker = createWorker();
        await worker.load();
        await worker.loadLanguage('eng');
        await worker.initialize('eng');
        const { data: { text } } = await worker.recognize(req.file.buffer);
        await worker.terminate();

        // Extract ingredient names from OCR text
        const ingredients = text.split('\n').filter(ingredient => ingredient.trim() !== '');

        // Lookup details of each ingredient
        const ingredientDetails = [];
        for (const ingredient of ingredients) {
            const response = await fetch(`http://localhost:3000/ingredients/${ingredient}`);
            const data = await response.json();
            ingredientDetails.push(...data);
        }

        // Respond with ingredient details
        res.json(ingredientDetails);
    } catch (error) {
        console.error(error);
        res.status(500).json({ message: 'Internal server error' });
    }
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
});
