const express = require('express');
const router = express.Router();
const axios = require('axios');
const fs = require('fs');
const path = require('path');

const TOGETHER_API_KEY = "0097473bda6ba5d1b430afc0cefdcbd87820c51bbd6a64d6ce6cb33cc1ee9acc";

const styles = [
  "Make it poetic.",
  "Make it sound like a sports coach.",
  "Make it gentle and nurturing.",
  "Make it sound like a wise old mentor.",
  "Make it short and punchy.",
  "Use a metaphor related to nature."
];

function getRandomStyle() {
  return styles[Math.floor(Math.random() * styles.length)];
}

router.post('/', async (req, res) => {
  const { challenge, behavior, tone, routine } = req.body;

  try {
    const randomStyle = getRandomStyle();
    const systemPrompt = `
You are a creative and insightful mindset coach for traders.
Each time, generate a truly unique, highly personalized affirmation that is different in style, structure, and language from previous ones.
Vary the sentence structure, use metaphors, analogies, or different tones (gentle, motivational, poetic, etc).
Never use the same sentence structure or opening lines as previous affirmations. Avoid repeating phrases, and do not use the phrase "I am confident and capable", "I wait for my confirmations with ease and grace", or similar templates. Start each affirmation in a completely new way. Do not start with "I am" or "You are". Begin with a metaphor, a question, or a vivid image.
Draw on the user's details to make each affirmation feel fresh and original.
`;
    const userPrompt = `
I'm a trader facing the following challenge: ${challenge}.
I'd like to work on this behavior: ${behavior}.
I prefer the affirmation to have a ${tone} tone and to be used as a ${routine}.
${randomStyle}
Please surprise me with something original and different from what you've written before.
`;

    const response = await axios.post(
      'https://api.together.xyz/v1/chat/completions',
      {
        model: "deepseek-ai/DeepSeek-R1-Distill-Llama-70B-free",
        messages: [
          { role: "system", content: systemPrompt },
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

    const outputPath = path.join(__dirname, '../../data/affirmation_log.json');
    const outputData = {
      timestamp: new Date().toISOString(),
      challenge,
      behavior,
      tone,
      routine,
      style: randomStyle,
      affirmation: response.data.choices[0].message.content
    };
    fs.writeFileSync(outputPath, JSON.stringify(outputData, null, 2));

    res.json({ affirmation: response.data.choices[0].message.content });
  } catch (err) {
    res.status(500).json({ error: err.message, details: err.response?.data });
  }
});

module.exports = router;
