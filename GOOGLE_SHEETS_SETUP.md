# Google Sheets Integration Setup Guide

## 🚀 Quick Setup Steps

### 1. Create Google Sheets
1. Go to [Google Sheets](https://sheets.google.com)
2. Create a new spreadsheet called "Mind2Profit Beta Applications"
3. Add these headers in row 1:
   ```
   Timestamp | First Name | Last Name | Email | Trading Experience | Trading Style | Current Tools | Pain Points | Expectations | Time Commitment | Device Access | Social Media | Additional Info
   ```

### 2. Get Spreadsheet ID
1. Copy the URL of your spreadsheet
2. Extract the ID (the long string between `/d/` and `/edit`)
3. Example: `https://docs.google.com/spreadsheets/d/1ABC123.../edit` → ID is `1ABC123...`

### 3. Set Up Google Cloud Project
1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Create a new project or select existing one
3. Enable Google Sheets API:
   - Go to "APIs & Services" → "Library"
   - Search for "Google Sheets API"
   - Click "Enable"

### 4. Create Service Account (Recommended)
1. Go to "APIs & Services" → "Credentials"
2. Click "Create Credentials" → "Service Account"
3. Fill in details and create
4. Click on the service account → "Keys" → "Add Key" → "Create New Key" → "JSON"
5. Download the JSON file and save as `service-account-key.json` in your backend folder
6. Share your Google Sheet with the service account email (found in the JSON file)

### 5. Environment Variables
Add these to your `.env` file:
```env
GOOGLE_SHEETS_SPREADSHEET_ID=your_spreadsheet_id_here
```

### 6. Install Dependencies
```bash
cd backend
pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client
```

## 📊 Alternative: Google Forms (Even Simpler!)

If you prefer an even simpler approach:

### 1. Create Google Form
1. Go to [Google Forms](https://forms.google.com)
2. Create a form with the same fields as your application
3. Set up the form to save responses to a Google Sheet

### 2. Replace Custom Form
1. Share the Google Form link instead of your custom form
2. Responses automatically go to Google Sheets
3. No backend integration needed!

## 🔧 Testing the Integration

### Test API Endpoint:
```bash
curl -X POST http://localhost:8000/api/beta-application \
  -H "Content-Type: application/json" \
  -d '{
    "firstName": "Test",
    "lastName": "User",
    "email": "test@example.com",
    "tradingExperience": "intermediate",
    "tradingStyle": "day-trading",
    "painPoints": "Psychology",
    "expectations": "Better tools",
    "timeCommitment": "3-5-hours",
    "deviceAccess": ["desktop", "mobile"]
  }'
```

### View Applications:
```bash
curl http://localhost:8000/api/beta-applications
```

## 📧 Email Notifications

The system will still send email notifications when applications are submitted. Make sure your `.env` file has:
```env
SENDER_EMAIL=your-email@gmail.com
SENDER_PASSWORD=your-app-password
RECIPIENT_EMAIL=kushkeswani@mind2profit.com
```

## 🎯 Benefits of Google Sheets

✅ **Easy to view** - Familiar spreadsheet interface  
✅ **Real-time updates** - See applications as they come in  
✅ **Easy filtering** - Sort by any column  
✅ **No database setup** - Much simpler than Supabase  
✅ **Automatic backups** - Google handles data safety  
✅ **Mobile friendly** - View on any device  

## 🚨 Troubleshooting

### Common Issues:
1. **Permission denied** - Make sure to share the sheet with the service account email
2. **API not enabled** - Ensure Google Sheets API is enabled in your project
3. **Wrong spreadsheet ID** - Double-check the ID in your .env file
4. **Service account key missing** - Ensure the JSON file is in the backend folder

### Debug Mode:
Add this to your `.env` file to see detailed logs:
```env
DEBUG=true
```

## 📱 Viewing Applications

Once set up, you can view applications by:
1. **Direct Google Sheets access** - Open the spreadsheet
2. **API endpoint** - `GET /api/beta-applications`
3. **Email notifications** - Get alerts for each submission

The Google Sheets approach is much simpler than Supabase and gives you a familiar interface to manage applications!
