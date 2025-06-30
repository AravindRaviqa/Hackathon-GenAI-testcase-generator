#!/usr/bin/env python3
"""
Troubleshooting script for Teams/Slack webhook issues
"""

import os
import requests
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def check_teams_webhook():
    """Check Teams webhook configuration and connectivity"""
    print("🔍 Troubleshooting Teams Webhook")
    print("=" * 40)
    
    teams_url = os.getenv('TEAMS_WEBHOOK_URL')
    
    if not teams_url:
        print("❌ TEAMS_WEBHOOK_URL not found in .env file")
        print("\n📝 To fix this:")
        print("1. Add TEAMS_WEBHOOK_URL to your .env file")
        print("2. Get the webhook URL from Teams:")
        print("   - Go to your Teams channel")
        print("   - Click '...' > Connectors")
        print("   - Configure 'Incoming Webhook'")
        print("   - Copy the webhook URL")
        return False
    
    print(f"✅ TEAMS_WEBHOOK_URL found: {teams_url[:50]}...")
    
    # Check URL format
    if not teams_url.startswith('https://'):
        print("❌ Webhook URL must start with 'https://'")
        return False
    
    if 'webhook.office.com' not in teams_url:
        print("❌ URL doesn't look like a valid Teams webhook")
        print("   Expected format: https://your-org.webhook.office.com/webhookb2/...")
        return False
    
    # Test connectivity
    print("\n🧪 Testing webhook connectivity...")
    
    test_message = {
        "@type": "MessageCard",
        "@context": "http://schema.org/extensions",
        "themeColor": "00FF00",
        "summary": "Test Message",
        "sections": [
            {
                "activityTitle": "🧪 Test Notification",
                "text": "This is a test message from Focaloid GenAI-Powered Quality Engineering Tools"
            }
        ]
    }
    
    try:
        response = requests.post(teams_url, json=test_message, timeout=10)
        print(f"📡 Response Status: {response.status_code}")
        print(f"📄 Response Content: {response.text}")
        
        if response.status_code == 200:
            print("✅ Teams webhook test successful!")
            return True
        elif response.status_code == 404:
            print("❌ Webhook URL not found (404)")
            print("   - Check if the webhook URL is correct")
            print("   - Make sure the webhook is still active in Teams")
            return False
        elif response.status_code == 403:
            print("❌ Webhook access denied (403)")
            print("   - Check if the webhook has proper permissions")
            print("   - Try creating a new webhook")
            return False
        else:
            print(f"❌ Unexpected response: {response.status_code}")
            return False
            
    except requests.exceptions.Timeout:
        print("❌ Request timed out")
        print("   - Check your internet connection")
        print("   - Try again later")
        return False
    except requests.exceptions.ConnectionError:
        print("❌ Connection error")
        print("   - Check your internet connection")
        print("   - Check if the webhook URL is accessible")
        return False
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def check_slack_webhook():
    """Check Slack webhook configuration and connectivity"""
    print("\n🔍 Troubleshooting Slack Webhook")
    print("=" * 40)
    
    slack_url = os.getenv('SLACK_WEBHOOK_URL')
    
    if not slack_url:
        print("❌ SLACK_WEBHOOK_URL not found in .env file")
        print("\n📝 To fix this:")
        print("1. Add SLACK_WEBHOOK_URL to your .env file")
        print("2. Get the webhook URL from Slack:")
        print("   - Go to api.slack.com/apps")
        print("   - Create New App > From scratch")
        print("   - Enable 'Incoming Webhooks'")
        print("   - Create webhook for your channel")
        print("   - Copy the webhook URL")
        return False
    
    print(f"✅ SLACK_WEBHOOK_URL found: {slack_url[:50]}...")
    
    # Check URL format
    if not slack_url.startswith('https://hooks.slack.com/'):
        print("❌ URL doesn't look like a valid Slack webhook")
        print("   Expected format: https://hooks.slack.com/services/...")
        return False
    
    # Test connectivity
    print("\n🧪 Testing webhook connectivity...")
    
    test_message = {
        "text": "🧪 Test message from Focaloid GenAI-Powered Quality Engineering Tools"
    }
    
    try:
        response = requests.post(slack_url, json=test_message, timeout=10)
        print(f"📡 Response Status: {response.status_code}")
        print(f"📄 Response Content: {response.text}")
        
        if response.status_code == 200:
            print("✅ Slack webhook test successful!")
            return True
        else:
            print(f"❌ Slack webhook test failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def main():
    """Main troubleshooting function"""
    print("🔧 Webhook Troubleshooting Tool")
    print("=" * 50)
    
    # Check .env file
    if not os.path.exists('.env'):
        print("❌ .env file not found")
        print("📝 Create a .env file with your webhook URLs")
        return
    
    print("✅ .env file found")
    
    # Test Teams webhook
    teams_ok = check_teams_webhook()
    
    # Test Slack webhook
    slack_ok = check_slack_webhook()
    
    # Summary
    print("\n📊 Summary:")
    print("=" * 20)
    print(f"Teams Webhook: {'✅ Working' if teams_ok else '❌ Failed'}")
    print(f"Slack Webhook: {'✅ Working' if slack_ok else '❌ Failed'}")
    
    if teams_ok and slack_ok:
        print("\n🎉 All webhooks are working! You can now use notifications.")
    else:
        print("\n🔧 Fix the issues above before using notifications.")

if __name__ == "__main__":
    main() 