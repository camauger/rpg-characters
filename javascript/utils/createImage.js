require('dotenv').config();
const openai = require('openai');
const axios = require('axios');
const fs = require('fs');

openai.apiKey = process.env.API_KEY;

async function createImage(prompt, id) {
    try {
        const response = await openai.Image.create({
            model: "dall-e-3",
            prompt: `I NEED to test how the tool works with extremely simple prompts. DO NOT add any detail, just use it AS-IS: ${prompt}`,
            size: "1024x1024",
            quality: "standard",
            n: 1,
        });

        const imageUrl = response.data[0].url;

        // Download the image to the static folder
        const r = await axios.get(imageUrl, { responseType: 'stream' });

        if (r.status === 200) {
            // Write to file in chunks (better for large files)
            const writer = fs.createWriteStream(`static/images/${id}.png`);
            r.data.pipe(writer);

            return new Promise((resolve, reject) => {
                writer.on('finish', resolve);
                writer.on('error', reject);
            });
        } else {
            console.log(`Unable to download image. HTTP Status Code: ${r.status}`);
        }
    } catch (e) {
        console.error(`Error occurred: ${e.message}`);
    }
}

module.exports = { createImage };
