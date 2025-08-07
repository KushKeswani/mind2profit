const express = require('express');
const router = express.Router();
const axios = require('axios');

const TOGETHER_API_KEY = "0097473bda6ba5d1b430afc0cefdcbd87820c51bbd6a64d6ce6cb33cc1ee9acc";

router.post('/', async (req, res) => {
  const { challenge, behavior, tone, routine } = req.body;
  try {
    const userPrompt = `My biggest trading challenge is: ${challenge}. I want to change or reinforce this behavior: ${behavior}. I want the affirmation to have a(n) ${tone} tone and be for my ${routine}.`;
    const response = await axios.post(
      'https://api.together.xyz/v1/chat/completions',
      {
        model: "meta-llama/Llama-3.3-70B-Instruct-Turbo-Free",
        messages: [
          { role: "system", content: "You are a mindset coach for traders. Generate a unique, short, and highly personalized affirmation for the user's situation. Use the details provided to make it specific and fresh every time." },
          { role: "user", content: userPrompt }
        ],
        temperature: 0.9,
        max_tokens: 120
      },
      {
        headers: {
          "Authorization": `Bearer ${TOGETHER_API_KEY}`,
          "Content-Type": "application/json"
        }
      }
    );
    res.json({ affirmation: response.data.choices[0].message.content });
  } catch (err) {
    res.status(500).json({ error: err.message, details: err.response?.data });
  }
});

module.exports = router;
