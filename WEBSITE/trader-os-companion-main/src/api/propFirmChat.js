const express = require('express');
const router = express.Router();
const axios = require('axios');

const TOGETHER_API_KEY = "0097473bda6ba5d1b430afc0cefdcbd87820c51bbd6a64d6ce6cb33cc1ee9acc";

router.post('/', async (req, res) => {
  const { message } = req.body;
  try {
    const response = await axios.post(
      'https://api.together.xyz/v1/chat/completions',
      {
        model: "meta-llama/Llama-3.3-70B-Instruct-Turbo-Free",
        messages: [
          { role: "system", content: "You are a prop firm trading expert. You know all the rules for FTMO, MyForexFunds, Topstep, and similar firms. Give clear, actionable advice and always reference the relevant rule if asked. If the user asks about daily loss, max drawdown, profit targets, or trading days, answer with specifics. If they ask for tips, give practical, rule-compliant advice." },
          { role: "user", content: message }
        ],
        temperature: 0.7,
        max_tokens: 200
      },
      {
        headers: {
          "Authorization": `Bearer ${TOGETHER_API_KEY}`,
          "Content-Type": "application/json"
        }
      }
    );
    res.json({ reply: response.data.choices[0].message.content });
  } catch (err) {
    res.status(500).json({ error: err.message, details: err.response?.data });
  }
});

module.exports = router;
