import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# Supabase configuration
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_ANON_KEY')

def get_supabase_client():
    """Get Supabase client"""
    try:
        # Try to import Supabase dependencies
        from supabase import create_client, Client
        
        if not SUPABASE_URL or not SUPABASE_KEY:
            print("Supabase credentials not configured. Check SUPABASE_URL and SUPABASE_ANON_KEY in .env")
            return None
        
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        return supabase
    except ImportError:
        print("Supabase dependencies not installed. Install with: pip install supabase")
        return None
    except Exception as e:
        print(f"Error setting up Supabase client: {e}")
        return None

def insert_beta_application(application_data: dict) -> dict:
    """Insert a new beta application into Supabase"""
    try:
        supabase = get_supabase_client()
        if not supabase:
            print("Supabase not configured. Applications will be saved to file instead.")
            return None
        
        # Prepare data for insertion - matching your actual column names
        data = {
            'additional_info': application_data.get('additionalInfo', ''),
            'trading_experience': application_data.get('tradingExperience', ''),
            'trading_style': application_data.get('tradingStyle', ''),
            'current_tools': application_data.get('currentTools', ''),
            'social_media': application_data.get('socialMedia', ''),
            'first_name': application_data.get('firstName', ''),
            'last_name': application_data.get('lastName', ''),
            'email': application_data.get('email', ''),
            'pain_points': application_data.get('painPoints', ''),
            'expectations': application_data.get('expectations', ''),
            'time_commitment': application_data.get('timeCommitment', ''),
            'device_access': application_data.get('deviceAccess', [])
        }
        
        # Insert into beta_applications table
        result = supabase.table('beta_applications').insert(data).execute()
        
        if result.data and len(result.data) > 0:
            inserted_record = result.data[0]
            # Handle the id field properly - it's 'id UUID' with a space
            record_id = inserted_record.get('id UUID')
            print(f"Application inserted into Supabase: {record_id}")
            return inserted_record
        else:
            print("Failed to insert application into Supabase")
            return None
            
    except Exception as e:
        print(f"Error inserting application into Supabase: {e}")
        return None

def get_beta_applications() -> list:
    """Get all beta applications from Supabase"""
    try:
        supabase = get_supabase_client()
        if not supabase:
            print("Supabase not configured. Returning empty list.")
            return []
        
        # Get all applications, ordered by created_at desc
        result = supabase.table('beta_applications').select('*').order('created_at', desc=True).execute()
        
        if result.data:
            # Transform data to match expected format
            applications = []
            for app in result.data:
                # Handle the id field properly - it's 'id UUID' with a space
                record_id = app.get('id UUID')
                application = {
                    'id': str(record_id),
                    'timestamp': app['created_at'],
                    'application': {
                        'firstName': app['first_name'],
                        'lastName': app['last_name'],
                        'email': app['email'],
                        'tradingExperience': app['trading_experience'],
                        'tradingStyle': app['trading_style'],
                        'currentTools': app['current_tools'],
                        'painPoints': app['pain_points'],
                        'expectations': app['expectations'],
                        'timeCommitment': app['time_commitment'],
                        'deviceAccess': app.get('device_access', []),
                        'socialMedia': app['social_media'],
                        'additionalInfo': app['additional_info']
                    }
                }
                applications.append(application)
            
            return applications
        else:
            return []
            
    except Exception as e:
        print(f"Error getting applications from Supabase: {e}")
        return []

def get_beta_application(application_id: str) -> dict:
    """Get a specific beta application by ID"""
    try:
        supabase = get_supabase_client()
        if not supabase:
            return None
        
        result = supabase.table('beta_applications').select('*').eq('id UUID', application_id).execute()
        
        if result.data:
            app = result.data[0]
            # Handle the id field properly - it's 'id UUID' with a space
            record_id = app.get('id UUID')
            return {
                'id': str(record_id),
                'timestamp': app['created_at'],
                'application': {
                    'firstName': app['first_name'],
                    'lastName': app['last_name'],
                    'email': app['email'],
                    'tradingExperience': app['trading_experience'],
                    'tradingStyle': app['trading_style'],
                    'currentTools': app['current_tools'],
                    'painPoints': app['pain_points'],
                    'expectations': app['expectations'],
                    'timeCommitment': app['time_commitment'],
                    'deviceAccess': app.get('device_access', []),
                    'socialMedia': app['social_media'],
                    'additionalInfo': app['additional_info']
                }
            }
        else:
            return None
            
    except Exception as e:
        print(f"Error getting application from Supabase: {e}")
        return None

def delete_beta_application(application_id: str) -> bool:
    """Delete a beta application"""
    try:
        supabase = get_supabase_client()
        if not supabase:
            return False
        
        result = supabase.table('beta_applications').delete().eq('id UUID', application_id).execute()
        
        if result.data:
            print(f"Application deleted from Supabase: {application_id}")
            return True
        else:
            print(f"Failed to delete application from Supabase: {application_id}")
            return False
            
    except Exception as e:
        print(f"Error deleting application from Supabase: {e}")
        return False

def insert_waitlist_email(email: str) -> dict:
    """Insert a new email into the waitlist table"""
    try:
        supabase = get_supabase_client()
        if not supabase:
            print("Supabase not configured. Waitlist emails will be saved to file instead.")
            return None
        
        # Prepare data for insertion
        data = {
            'email': email,
            'subscribed_at': datetime.now().isoformat(),
            'status': 'active'
        }
        
        # Insert into waitlist table
        result = supabase.table('waitlist').insert(data).execute()
        
        if result.data and len(result.data) > 0:
            inserted_record = result.data[0]
            record_id = inserted_record.get('id')
            print(f"Waitlist email inserted into Supabase: {record_id}")
            return inserted_record
        else:
            print("Failed to insert waitlist email into Supabase")
            return None
            
    except Exception as e:
        print(f"Error inserting waitlist email into Supabase: {e}")
        return None

def get_waitlist_emails() -> list:
    """Get all waitlist emails from Supabase"""
    try:
        supabase = get_supabase_client()
        if not supabase:
            print("Supabase not configured. Returning empty list.")
            return []
        
        # Get all waitlist emails, ordered by subscribed_at desc
        result = supabase.table('waitlist').select('*').order('subscribed_at', desc=True).execute()
        
        if result.data:
            return result.data
        else:
            return []
            
    except Exception as e:
        print(f"Error getting waitlist emails from Supabase: {e}")
        return []
