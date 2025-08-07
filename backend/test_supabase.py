import os
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_ANON_KEY')

print(f"SUPABASE_URL: {SUPABASE_URL}")
print(f"SUPABASE_KEY: {SUPABASE_KEY[:20]}..." if SUPABASE_KEY else "None")

try:
    from supabase import create_client, Client
    
    if not SUPABASE_URL or not SUPABASE_KEY:
        print("Missing Supabase credentials")
        exit(1)
    
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    print("Supabase client created successfully")
    
    # Test a simple query
    result = supabase.table('beta_applications').select('count').execute()
    print(f"Query result: {result}")
    
    # Test inserting a record
    test_data = {
        'additional_info': 'Test from script',
        'trading_experience': 'beginner',
        'trading_style': 'day-trading',
        'current_tools': 'Test tools',
        'social_media': '@test',
        'first_name': 'Test',
        'last_name': 'Script',
        'email': 'test@script.com',
        'pain_points': 'Testing RLS',
        'expectations': 'Should work',
        'time_commitment': '1-2-hours',
        'device_access': []
    }
    
    print("Attempting to insert test record...")
    insert_result = supabase.table('beta_applications').insert(test_data).execute()
    print(f"Insert result: {insert_result}")
    
    # Show the exact structure of the response
    if insert_result.data:
        print("\nFirst record structure:")
        first_record = insert_result.data[0]
        for key, value in first_record.items():
            print(f"  {key}: {value}")
    
except Exception as e:
    print(f"Error: {e}")
