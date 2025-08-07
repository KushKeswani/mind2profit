# Mind2Profit - Trading Platform

A comprehensive trading platform built with React frontend and FastAPI backend, featuring automated backtesting, manual backtesting, and beta tester applications.

## 🚀 Features

### Frontend (React + TypeScript)
- **Coming Soon Page**: Landing page with countdown to launch
- **About Page**: Detailed information about the platform and creator
- **Beta Tester Application**: Form for potential beta testers to apply
- **Responsive Design**: Modern UI with Tailwind CSS and Shadcn components
- **Authentication System**: Protected routes for paid users

### Backend (FastAPI + Python)
- **Automated Backtesting**: Multiple trading strategies (MACD, RSI, Bollinger Bands, etc.)
- **Manual Backtesting**: Custom strategy testing with Alpaca API
- **Beta Application System**: Supabase integration for storing applications
- **Economic Calendar**: Market data and economic events
- **Strategy Management**: Save, load, and compare trading strategies

## 🛠️ Tech Stack

### Frontend
- React 18
- TypeScript
- Vite
- Tailwind CSS
- Shadcn UI
- React Router DOM
- Lucide React Icons

### Backend
- FastAPI
- Python 3.9
- Uvicorn
- Pandas
- NumPy
- Technical Analysis Library
- Alpaca API
- Supabase
- YFinance

## 📦 Installation

### Prerequisites
- Node.js 18+
- Python 3.9+
- Git

### Frontend Setup
```bash
cd WEBSITE/trader-os-companion-main
npm install
npm run dev
```

### Backend Setup
```bash
cd backend
python -m venv backend-venv
source backend-venv/bin/activate  # On Windows: backend-venv\Scripts\activate
pip install -r requirements.txt
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## 🔧 Environment Variables

Create a `.env` file in the backend directory:

```env
SUPABASE_URL=your_supabase_url
SUPABASE_ANON_KEY=your_supabase_anon_key
SENDER_EMAIL=your_email@gmail.com
SENDER_PASSWORD=your_app_password
RECIPIENT_EMAIL=admin@mind2profit.com
DEBUG=true
```

## 🚀 Deployment

### Frontend (Vercel)
1. Push code to GitHub
2. Connect repository to Vercel
3. Set environment variables in Vercel dashboard
4. Deploy

### Backend (Railway/Render)
1. Connect GitHub repository
2. Set environment variables
3. Deploy

## 📁 Project Structure

```
TRADEROS/
├── backend/                 # FastAPI backend
│   ├── main.py             # Main application entry
│   ├── requirements.txt     # Python dependencies
│   ├── strategy_api.py     # Automated backtesting
│   ├── manual_backtest_api.py  # Manual backtesting
│   ├── beta_application_api.py  # Beta tester applications
│   └── supabase_api.py     # Supabase integration
├── WEBSITE/
│   └── trader-os-companion-main/  # React frontend
│       ├── src/
│       │   ├── pages/      # React pages
│       │   ├── components/ # UI components
│       │   └── contexts/   # React contexts
│       └── package.json
└── README.md
```

## 🎯 Current Status

- ✅ Frontend: Coming Soon page, About page, Beta application form
- ✅ Backend: Automated backtesting, manual backtesting, Supabase integration
- ✅ Beta Application System: Working with Supabase database
- 🔄 Deployment: Ready for Vercel deployment

## 📞 Contact

- Email: kushkeswani@mind2profit.com
- Platform: Mind2Profit

## 📄 License

This project is proprietary software. All rights reserved.
