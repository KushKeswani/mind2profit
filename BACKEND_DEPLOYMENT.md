# Backend Deployment Guide

## 🎯 Current Status

- ✅ **Frontend**: Live on `mind2profit.com` (Vercel) - 24/7
- 🔄 **Backend**: Local only (localhost:8000) - stops when computer is off

## 🚀 Deploy Backend Options

### Option 1: Railway (Recommended)
```bash
# 1. Go to railway.app
# 2. Connect GitHub repository
# 3. Deploy from backend/ directory
# 4. Set environment variables
# 5. Get production URL (e.g., https://mind2profit-backend.railway.app)
```

### Option 2: Heroku
```bash
# 1. Install Heroku CLI
# 2. Create Procfile in backend/
# 3. Deploy: heroku create mind2profit-api
# 4. Push: git push heroku main
```

### Option 3: Vercel Functions
```bash
# 1. Convert to serverless functions
# 2. Deploy as Vercel Functions
# 3. Integrate with existing frontend
```

## 🔧 Environment Setup

### Required Environment Variables
```bash
# Supabase (optional)
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key

# API Keys (optional)
FRED_API_KEY=your_fred_key
TRADING_ECONOMICS_API_KEY=your_key

# Security
SECRET_KEY=your_secret_key
JWT_SECRET=your_jwt_secret
```

## 📊 Update Frontend to Use Production Backend

Once backend is deployed, update frontend:
```javascript
// Change from:
const API_URL = 'http://localhost:8000'

// To:
const API_URL = 'https://your-backend-url.railway.app'
```

## 🎉 Result

- ✅ **Frontend**: `mind2profit.com` (Vercel) - 24/7
- ✅ **Backend**: `your-backend-url.railway.app` - 24/7
- ✅ **Complete App**: Works when computer is off!
