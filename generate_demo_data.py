"""
Generate demo data for the Customer Behavior Analytics dashboard.
This creates sample user interactions to showcase the analytics capabilities.
"""

import requests
import random
import time
from datetime import datetime, timedelta

# API endpoint - change this to your deployed API URL
API_URL = "http://localhost:5001/api/track"

# Sample data
USER_IDS = [f"user_{i:03d}" for i in range(1, 51)]  # 50 users
ACTIONS = ["page_view", "click", "scroll", "hover", "submit", "search", "download"]
PAGES = ["/home", "/products", "/about", "/contact", "/pricing", "/features", "/blog", "/login", "/signup"]

def generate_interaction():
    """Generate a random user interaction."""
    return {
        "user_id": random.choice(USER_IDS),
        "action": random.choice(ACTIONS),
        "page": random.choice(PAGES),
        "metadata": {
            "session_duration": random.randint(10, 300),
            "device": random.choice(["desktop", "mobile", "tablet"]),
            "referrer": random.choice(["google", "facebook", "direct", "twitter"])
        }
    }

def send_interaction(interaction):
    """Send interaction to the API."""
    try:
        response = requests.post(API_URL, json=interaction)
        if response.status_code == 201:
            print(f"✅ Tracked: {interaction['user_id']} - {interaction['action']} on {interaction['page']}")
            return True
        else:
            print(f"❌ Error: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"❌ Connection error: {str(e)}")
        print("Make sure the Flask API is running at", API_URL)
        return False

def generate_demo_data(num_interactions=100, delay=0.1):
    """
    Generate demo data for the dashboard.
    
    Args:
        num_interactions: Number of interactions to generate
        delay: Delay between requests in seconds
    """
    print(f"🚀 Generating {num_interactions} demo interactions...")
    print(f"API URL: {API_URL}")
    print("-" * 60)
    
    successful = 0
    failed = 0
    
    for i in range(num_interactions):
        interaction = generate_interaction()
        
        if send_interaction(interaction):
            successful += 1
        else:
            failed += 1
            if failed >= 3:
                print("\n⚠️  Multiple failures detected. Please check:")
                print("   1. Is the Flask API running? (python app.py)")
                print("   2. Is the API_URL correct?")
                print(f"   3. Current API_URL: {API_URL}")
                break
        
        time.sleep(delay)
        
        # Progress update
        if (i + 1) % 10 == 0:
            print(f"Progress: {i + 1}/{num_interactions} interactions sent")
    
    print("-" * 60)
    print(f"✅ Successfully sent: {successful}")
    print(f"❌ Failed: {failed}")
    print(f"📊 View your dashboard at: http://localhost:8501")

if __name__ == "__main__":
    print("=" * 60)
    print("Customer Behavior Analytics - Demo Data Generator")
    print("=" * 60)
    print()
    
    # Check if custom API URL is needed
    custom_url = input("Press Enter to use default (http://localhost:5001/api/track)\nOr enter custom API URL: ").strip()
    if custom_url:
        API_URL = custom_url if custom_url.endswith("/track") else f"{custom_url}/api/track"
        print(f"Using custom URL: {API_URL}")
    
    print()
    
    # Generate data
    try:
        generate_demo_data(num_interactions=100, delay=0.1)
        print()
        print("🎉 Demo data generation complete!")
        print("💡 Refresh your Streamlit dashboard to see the new data")
    except KeyboardInterrupt:
        print("\n\n⚠️  Generation interrupted by user")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
