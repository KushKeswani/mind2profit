require('dotenv').config();
const express = require('express');
const path = require('path');
const app = express();

app.use(express.json());

// Serve static files from frontend build (if using build)
app.use(express.static(path.join(__dirname, 'build')));

// API route for affirmation generation
app.use('/api/generateAffirmation', require('./src/api/generateAffirmation.cjs'));
app.use('/api/togetherAffirmation', require('./src/api/togetherAffirmation.cjs'));
app.use('/api/propFirmChat', require('./src/api/propFirmChat.cjs'));

// Fallback to frontend for any other route
app.get('*', (req, res) => {
  res.sendFile(path.join(__dirname, 'build', 'index.html'));
});

const PORT = process.env.PORT || 3001;
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
