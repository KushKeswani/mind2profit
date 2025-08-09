# Mind2Profit Update Workflow

## 🚀 Quick Update Commands

### Frontend Updates
```bash
# Navigate to frontend
cd WEBSITE/mind2profit-publish-main

# Make your changes (edit files)

# Test locally
npm run dev

# Commit and push
git add .
git commit -m "Update frontend: [describe changes]"
git push origin main
```

### Backend Updates
```bash
# Navigate to backend
cd backend

# Make your changes (edit Python files)

# Test locally
source venv/bin/activate
uvicorn main:app --reload --host 127.0.0.1 --port 8000

# Commit and push
git add .
git commit -m "Update backend: [describe changes]"
git push origin main
```

### Content Updates (Meta tags, text, images)
```bash
# Edit content files
cd WEBSITE/mind2profit-publish-main

# Update meta tags, text content, images
git add .
git commit -m "Update content: [describe changes]"
git push origin main
```

## 🎯 Automatic Deployment

- **Frontend**: Vercel automatically deploys to `mind2profit.com` in 2-5 minutes
- **Backend**: Needs separate deployment (Railway, Heroku, or Vercel Functions)

## 📊 Check Deployments

- **Frontend**: Visit `https://mind2profit.com` to see live changes
- **Backend**: Check `http://localhost:8000` for local testing
- **Waitlist**: Visit `http://localhost:8000/admin/waitlist` for admin view

## 🔧 Troubleshooting

### If changes don't appear:
1. Check Vercel dashboard for build status
2. Clear browser cache or try incognito
3. Wait 5-10 minutes for propagation

### If backend issues:
1. Restart local server: `uvicorn main:app --reload`
2. Check logs for errors
3. Verify dependencies: `pip install -r requirements.txt`
