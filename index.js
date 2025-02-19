const express = require("express");
const axios = require("axios");
require("dotenv").config();

const app = express();
const port = process.env.PORT || 3000;

app.use(express.json());

app.get("/", (req, res) => {
    res.send("AI Image Generator API is running.");
});

app.post("/generate", async (req, res) => {
    const { prompt } = req.body;

    if (!prompt) {
        return res.status(400).json({ error: "Prompt is required" });
    }

    try {
        const response = await axios.post(
            "https://api.replicate.com/v1/predictions",
            {
                version: "stability-ai/stable-diffusion",
                input: { prompt: prompt }
            },
            {
                headers: {
                    Authorization: `Token ${process.env.REPLICATE_API_TOKEN}`,
                    "Content-Type": "application/json"
                }
            }
        );

        res.json(response.data);
    } catch (error) {
        console.error("Error generating image:", error.response ? error.response.data : error.message);
        res.status(500).json({ error: "Failed to generate image" });
    }
});

app.listen(port, () => {
    console.log(`Server running on port ${port}`);
});

module.exports = app;
