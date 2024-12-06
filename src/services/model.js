const axios = require('axios');

async function analyzeImage(imageUrl) {
    try {
        const response = await axios.post('https://model-api-url/analyze', { imageUrl });
        return response.data;
    } catch (error) {
        console.error('Error analyzing image:', error.message);
        throw new Error('Failed to analyze image');
    }
}

module.exports = { analyzeImage };
