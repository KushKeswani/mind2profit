// Simple Node.js/Express API route for OpenAI GPT-4 affirmation generation
// Place your API key in an environment variable for security

const express = require('express');
const router = express.Router();
const axios = require('axios');

// Load API key from environment variable
const OPENAI_API_KEY = process.env.OPENAI_API_KEY;

router.post('/', async (req, res) => {
  const { tradingIssue, desiredMindset, personalAddons } = req.body;

  const prompt = `You are a trading mindset coach who specializes in hypnosis-style affirmations. Write a realistic, calm, hypnosis-style affirmation transcript (8-12 lines) for a trader. Use second-person point of view. Encourage calm breathing, self-trust, discipline, and goal reminders. Reframe the negative habit into a positive trait. Make it sound like a meditation or guided self-talk. Avoid clichés. Make it specific to the input.\n\nTrading Issue: ${tradingIssue}\nDesired Mindset: ${desiredMindset}\nPersonal Add-ons: ${personalAddons || ''}`;

  try {
    const response = await axios.post(
      'https://api.openai.com/v1/chat/completions',
      {
        model: 'gpt-4',
        messages: [
          { role: 'system', content: 'You are a helpful trading mindset coach.' },
          { role: 'user', content: prompt }
        ],
        max_tokens: 350,
        temperature: 0.8
      },
      {
        headers: {
          'Authorization': `Bearer ${OPENAI_API_KEY}`,
          'Content-Type': 'application/json'
        }
      }
    );
    const transcript = response.data.choices[0].message.content;
    res.json({ transcript });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

module.exports = router;
