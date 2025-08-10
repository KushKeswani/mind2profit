# Heroku Deployment Guide

## 🚀 Quick Heroku Setup

### Step 1: Install Heroku CLI (Already Done)
```bash
# ✅ Already installed via Homebrew
heroku --version
```

### Step 2: Login to Heroku
```bash
# This will open your browser to login
heroku login
```

### Step 3: Create Heroku App
```bash
# Navigate to backend directory
cd backend

# Create Heroku app
heroku create mind2profit-api

# This will give you a URL like: https://mind2profit-api.herokuapp.com
```

### Step 4: Deploy to Heroku
```bash
# Push to Heroku
git push heroku main

# If you get an error about no Heroku remote, run:
heroku git:remote -a mind2profit-api
```

### Step 5: Open Your App
```bash
# Open your deployed app
heroku open
```

## 🔧 Environment Variables (Optional)

If you want to add environment variables:
```bash
# Add Supabase credentials (optional)
heroku config:set SUPABASE_URL=your_supabase_url
heroku config:set SUPABASE_KEY=your_supabase_key

# Add API keys (optional)
heroku config:set FRED_API_KEY=your_fred_key
```

## 🎯 Update Frontend

Once deployed, update your frontend to use the new backend URL:

1. **Go to Vercel Dashboard**
2. **Navigate to your project**
3. **Go to Settings → Environment Variables**
4. **Add new variable:**
   - Name: `VITE_API_URL`
   - Value: `https://mind2profit-api.herokuapp.com`

## ✅ Result

- **Frontend**: `mind2profit.com` (Vercel) - 24/7
- **Backend**: `https://mind2profit-api.herokuapp.com` - 24/7
- **Complete App**: Works when computer is off!

## 🆘 Troubleshooting

### If you get build errors:
```bash
# Check Heroku logs
heroku logs --tail

# Check if all dependencies are in requirements.txt
cat requirements.txt
```

### If you need to restart:
```bash
heroku restart
```

### If you need to check app status:
```bash
heroku ps
```
