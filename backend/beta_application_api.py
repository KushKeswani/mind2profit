from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import json
import os
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv
from supabase_api import insert_beta_application, get_beta_applications, get_beta_application, delete_beta_application

load_dotenv()

router = APIRouter()

class BetaApplication(BaseModel):
    firstName: str
    lastName: str
    email: str
    tradingExperience: str
    tradingStyle: str
    currentTools: Optional[str] = ""
    painPoints: str
    expectations: str
    timeCommitment: str
    deviceAccess: List[str]
    socialMedia: Optional[str] = ""
    additionalInfo: Optional[str] = ""

class BetaApplicationResponse(BaseModel):
    id: str
    timestamp: str
    application: BetaApplication

# Fallback file storage
APPLICATIONS_FILE = "beta_applications.json"

def load_applications_from_file():
    """Load existing applications from file"""
    if os.path.exists(APPLICATIONS_FILE):
        with open(APPLICATIONS_FILE, 'r') as f:
            return json.load(f)
    return []

def save_applications_to_file(applications):
    """Save applications to file"""
    with open(APPLICATIONS_FILE, 'w') as f:
        json.dump(applications, f, indent=2)

def send_email_notification(application: BetaApplication):
    """Send email notification about new application"""
    try:
        # Get email credentials from environment variables
        sender_email = os.getenv("SENDER_EMAIL")
        sender_password = os.getenv("SENDER_PASSWORD")
        recipient_email = os.getenv("RECIPIENT_EMAIL", "kushkeswani@mind2profit.com")
        
        if not sender_email or not sender_password:
            print("Email credentials not configured. Skipping email notification.")
            return
        
        # Create message
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = f"New Beta Tester Application: {application.firstName} {application.lastName}"
        
        # Create email body
        supabase_url = os.getenv('SUPABASE_URL')
        dashboard_link = f"{supabase_url}/dashboard" if supabase_url else "Check the applications file"
        
        body = f"""
        New Beta Tester Application Received!
        
        Name: {application.firstName} {application.lastName}
        Email: {application.email}
        Trading Experience: {application.tradingExperience}
        Trading Style: {application.tradingStyle}
        Time Commitment: {application.timeCommitment}
        Device Access: {', '.join(application.deviceAccess)}
        
        Current Tools: {application.currentTools}
        Pain Points: {application.painPoints}
        Expectations: {application.expectations}
        Social Media: {application.socialMedia}
        Additional Info: {application.additionalInfo}
        
        Submitted at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        
        View applications: {dashboard_link}
        """
        
        msg.attach(MIMEText(body, 'plain'))
        
        # Send email
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        text = msg.as_string()
        server.sendmail(sender_email, recipient_email, text)
        server.quit()
        
        print(f"Email notification sent for application from {application.email}")
        
    except Exception as e:
        print(f"Failed to send email notification: {e}")

@router.post("/beta-application")
async def submit_beta_application(application: BetaApplication):
    """Submit a new beta tester application"""
    try:
        # Try Supabase first
        supabase_result = insert_beta_application(application.dict())
        
        if supabase_result:
            # Successfully saved to Supabase
            send_email_notification(application)
            # Handle the id field properly - it's 'id UUID' with a space
            record_id = supabase_result.get('id UUID')
            return {"message": "Application submitted successfully", "id": str(record_id)}
        else:
            # Fall back to file storage
            applications = load_applications_from_file()
            
            new_application = {
                "id": f"app_{len(applications) + 1}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                "timestamp": datetime.now().isoformat(),
                "application": application.dict()
            }
            
            applications.append(new_application)
            save_applications_to_file(applications)
            
            send_email_notification(application)
            return {"message": "Application submitted successfully (saved to file)", "id": new_application["id"]}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to submit application: {str(e)}")

@router.get("/beta-applications")
async def get_all_beta_applications():
    """Get all beta applications"""
    try:
        # Try Supabase first
        supabase_applications = get_beta_applications()
        
        if supabase_applications:
            return {"applications": supabase_applications}
        else:
            # Fall back to file storage
            applications = load_applications_from_file()
            return {"applications": applications}
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to load applications: {str(e)}")

@router.get("/beta-applications/{application_id}")
async def get_specific_beta_application(application_id: str):
    """Get a specific beta application by ID"""
    try:
        # Try Supabase first
        supabase_application = get_beta_application(application_id)
        
        if supabase_application:
            return supabase_application
        else:
            # Fall back to file storage
            applications = load_applications_from_file()
            for app in applications:
                if app["id"] == application_id:
                    return app
                    
        raise HTTPException(status_code=404, detail="Application not found")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to load application: {str(e)}")

@router.delete("/beta-applications/{application_id}")
async def delete_specific_beta_application(application_id: str):
    """Delete a beta application"""
    try:
        # Try Supabase first
        supabase_success = delete_beta_application(application_id)
        
        if supabase_success:
            return {"message": "Application deleted successfully"}
        else:
            # Fall back to file storage
            applications = load_applications_from_file()
            applications = [app for app in applications if app["id"] != application_id]
            save_applications_to_file(applications)
            return {"message": "Application deleted successfully (from file)"}
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete application: {str(e)}")
