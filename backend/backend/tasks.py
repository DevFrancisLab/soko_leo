import os
from celery import shared_task
import africastalking
from django.contrib.auth.models import User
from ai.run_workflow import run_workflow_for_backend


@shared_task
def send_market_insights():
    """
    Periodic task that runs the AI workflow for all registered farmers
    and sends SMS alerts with market insights using Africa's Talking API.
    """
    # Initialize Africa's Talking
    username = os.getenv('AT_USERNAME', 'your_username')
    api_key = os.getenv('AT_API_KEY', 'your_api_key')
    
    africastalking.initialize(username, api_key)
    sms = africastalking.SMS
    
    # Get all users (assuming all are farmers for simplicity)
    users = User.objects.all()
    
    for user in users:
        # Get user's phone number from profile
        try:
            profile = user.profile
            phone = profile.phone
            if not phone:
                continue  # Skip if no phone
        except:
            continue  # Skip if no profile
        
        # Run workflow with sample/default data (in production, use user-specific data)
        market_data = "Current market prices show maize at KSh 3,800 per 90kg bag with +5% trend."
        weather_data = {
            "temperature": 24,
            "condition": "partly cloudy",
            "rainfall": 40
        }
        crop_data = {
            "crop_type": "maize",
            "yield_estimate": "high",
            "location": "Nairobi"
        }
        
        try:
            insights = run_workflow_for_backend(market_data, weather_data, crop_data)
            
            # Format message
            message = f"SokoLeo Insights:\nMarket: {insights.get('market_insight', 'N/A')}\nWeather: {insights.get('weather_insight', 'N/A')}\nCrop: {insights.get('crop_insight', 'N/A')}"
            
            # Send SMS
            response = sms.send(message, [phone])
            print(f"Sent insights to {phone}: {response}")
            
        except Exception as e:
            print(f"Error sending insights to {user.username}: {e}")
            continue