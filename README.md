# Mind2Profit - Trading Platform

A comprehensive trading platform built with React/TypeScript frontend and FastAPI backend.

## 🚀 Quick Start

### Prerequisites
- Node.js 18+ 
- Python 3.9+
- Git

### Backend Setup

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Create virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   ```bash
   cp env_template.txt .env
   # Edit .env with your actual API keys
   ```

5. **Start the backend:**
   ```bash
   python3 -m uvicorn main:app --reload --host 127.0.0.1 --port 8000
   ```

### Frontend Setup

1. **Navigate to frontend directory:**
   ```bash
   cd WEBSITE/mind2profit-companion-main
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Start the development server:**
   ```bash
   npm run dev
   ```

4. **Open your browser:**
   Navigate to `http://localhost:8080`

## 📁 Project Structure

```
mind2profit-clean/
├── backend/                 # FastAPI backend
│   ├── main.py             # Main application entry point
│   ├── requirements.txt    # Python dependencies
│   ├── env_template.txt   # Environment variables template
│   └── ...
├── WEBSITE/               # React frontend
│   └── mind2profit-companion-main/
│       ├── src/           # React components
│       ├── package.json   # Node.js dependencies
│       └── ...
├── CALANDER/             # Calendar resources
├── OG WEBSITE/           # Original website assets
└── README.md            # This file
```

## 🔧 Configuration

### Environment Variables

Copy `backend/env_template.txt` to `backend/.env` and configure:

- `SUPABASE_URL`: Your Supabase project URL
- `SUPABASE_KEY`: Your Supabase anonymous key
- `FRED_API_KEY`: Federal Reserve Economic Data API key (optional)
- `TRADING_ECONOMICS_API_KEY`: Trading Economics API key (optional)

### API Keys Setup

1. **Supabase**: Create a project at [supabase.com](https://supabase.com)
2. **FRED API**: Get free API key at [fred.stlouisfed.org](https://fred.stlouisfed.org)
3. **Trading Economics**: Get API key at [tradingeconomics.com](https://tradingeconomics.com)

## 🚀 Deployment

### Backend Deployment
- **Heroku**: Use the `Procfile` in the backend directory
- **Railway**: Connect your GitHub repository
- **Vercel**: Use the serverless functions approach

### Frontend Deployment
- **Vercel**: Connect your GitHub repository
- **Netlify**: Deploy from the `WEBSITE/mind2profit-companion-main` directory
- **GitHub Pages**: Build and deploy the dist folder

## 📚 Features

- **Trading Strategies**: Backtest and deploy trading strategies
- **Educational Content**: Comprehensive trading topics and learning resources
- **Real-time Data**: Live market data integration
- **User Management**: Authentication and user profiles
- **Analytics**: Performance tracking and analysis
- **Calendar Integration**: Economic calendar and events
- **AI Integration**: AI-powered trading insights

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit changes: `git commit -am 'Add feature'`
4. Push to branch: `git push origin feature-name`
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🔗 Links

- [Live Demo](https://mind2profit.com)
- [Documentation](https://docs.mind2profit.com)
- [API Reference](https://api.mind2profit.com/docs)

## 📞 Support

For support, email support@mind2profit.com or create an issue in this repository.
# Updated Mon Aug 11 14:38:27 EDT 2025
