import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# Google Sheets API setup
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = 'service-account-key.json'  # You'll need to create this
SPREADSHEET_ID = os.getenv('GOOGLE_SHEETS_SPREADSHEET_ID')
RANGE_NAME = 'Applications!A:M'  # Adjust based on your sheet structure

def get_sheets_service():
    """Get Google Sheets service"""
    try:
        # Try to import Google Sheets dependencies
        from google.oauth2.credentials import Credentials
        from googleapiclient.discovery import build
        from google.oauth2 import service_account
        
        if os.path.exists(SERVICE_ACCOUNT_FILE):
            creds = service_account.Credentials.from_service_account_file(
                SERVICE_ACCOUNT_FILE, scopes=SCOPES)
        else:
            # Fallback to environment variables
            creds = Credentials.from_authorized_user_info({
                'client_id': os.getenv('GOOGLE_CLIENT_ID'),
                'client_secret': os.getenv('GOOGLE_CLIENT_SECRET'),
                'refresh_token': os.getenv('GOOGLE_REFRESH_TOKEN'),
            }, SCOPES)
        
        service = build('sheets', 'v4', credentials=creds)
        return service
    except ImportError:
        print("Google Sheets dependencies not installed. Install with: pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client")
        return None
    except Exception as e:
        print(f"Error setting up Google Sheets service: {e}")
        return None

def append_application_to_sheets(application_data):
    """Append a new application to Google Sheets"""
    try:
        service = get_sheets_service()
        if not service:
            print("Google Sheets not configured. Applications will be saved to file instead.")
            return False
        
        # Prepare row data
        row_data = [
            datetime.now().strftime('%Y-%m-%d %H:%M:%S'),  # Timestamp
            application_data.get('firstName', ''),
            application_data.get('lastName', ''),
            application_data.get('email', ''),
            application_data.get('tradingExperience', ''),
            application_data.get('tradingStyle', ''),
            application_data.get('currentTools', ''),
            application_data.get('painPoints', ''),
            application_data.get('expectations', ''),
            application_data.get('timeCommitment', ''),
            ', '.join(application_data.get('deviceAccess', [])),
            application_data.get('socialMedia', ''),
            application_data.get('additionalInfo', '')
        ]
        
        # Append to sheet
        body = {
            'values': [row_data]
        }
        
        result = service.spreadsheets().values().append(
            spreadsheetId=SPREADSHEET_ID,
            range=RANGE_NAME,
            valueInputOption='RAW',
            insertDataOption='INSERT_ROWS',
            body=body
        ).execute()
        
        print(f"Application added to Google Sheets: {result.get('updates').get('updatedRows')} rows updated")
        return True
        
    except Exception as e:
        print(f"Error appending to Google Sheets: {e}")
        return False

def get_applications_from_sheets():
    """Get all applications from Google Sheets"""
    try:
        service = get_sheets_service()
        if not service:
            print("Google Sheets not configured. Returning empty list.")
            return []
        
        result = service.spreadsheets().values().get(
            spreadsheetId=SPREADSHEET_ID,
            range=RANGE_NAME
        ).execute()
        
        values = result.get('values', [])
        if not values:
            return []
        
        # Skip header row
        applications = []
        for i, row in enumerate(values[1:], 1):
            if len(row) >= 13:  # Ensure we have enough columns
                application = {
                    'id': f"sheet_row_{i}",
                    'timestamp': row[0],
                    'application': {
                        'firstName': row[1],
                        'lastName': row[2],
                        'email': row[3],
                        'tradingExperience': row[4],
                        'tradingStyle': row[5],
                        'currentTools': row[6],
                        'painPoints': row[7],
                        'expectations': row[8],
                        'timeCommitment': row[9],
                        'deviceAccess': row[10].split(', ') if row[10] else [],
                        'socialMedia': row[11],
                        'additionalInfo': row[12]
                    }
                }
                applications.append(application)
        
        return applications
        
    except Exception as e:
        print(f"Error getting applications from Google Sheets: {e}")
        return []
