#!/usr/bin/env python3
"""
Test script to demonstrate the Slack/Teams notification feature
"""

def test_notification_features():
    """Test the notification functionality"""
    
    print("📢 Testing Slack/Teams Notification Feature")
    print("=" * 50)
    
    # Sample notification scenarios
    scenarios = [
        {
            "name": "High Severity Bug",
            "log": """
[ERROR] Test failed: UserService.test_create_user
HTTPError: 500 Internal Server Error
POST /api/users
Response: {"error": "Database connection failed"}
File: /src/services/UserService.java
            """,
            "severity": "High",
            "assignee_type": "Backend Developer"
        },
        {
            "name": "Medium Severity UI Issue",
            "log": """
[ERROR] Test failed: LoginPage.test_user_login
AssertionError: Expected element with id 'dashboard-welcome' to be visible
File: /src/components/LoginPage.js
            """,
            "severity": "Medium", 
            "assignee_type": "Frontend Developer"
        }
    ]
    
    for i, scenario in enumerate(scenarios, 1):
        print(f"\n📝 Scenario {i}: {scenario['name']}")
        print(f"🎯 Severity: {scenario['severity']}")
        print(f"👤 Assignee Type: {scenario['assignee_type']}")
        
        # Simulate notification message
        print("\n📨 Notification Message Preview:")
        print("-" * 40)
        
        if scenario['severity'] == 'High':
            color = "🔴"
            theme_color = "#FF0000"
        elif scenario['severity'] == 'Medium':
            color = "🟡"
            theme_color = "#FFA500"
        else:
            color = "🟢"
            theme_color = "#00FF00"
        
        notification_preview = f"""
{color} Bug Triage Alert

📋 Failure: {scenario['name']}
🚨 Severity: {scenario['severity']}
👤 Assignee Type: {scenario['assignee_type']}

📄 Log Summary: {scenario['log'][:100]}...

🔍 Suggested Assignees:
📁 src/services/UserService.java: John Developer (@johndev) 🔴
📁 src/components/LoginPage.js: Jane Designer (@janedesign) 🟡

💡 Assignment Strategy:
• Primary Expert: John Developer (@johndev) - 8 recent commits
• Team Involvement: 3 contributors involved
• Moderate Activity: Recent contributor should handle this

🔗 View in Focaloid GenAI Tools: http://localhost:5000
        """
        
        print(notification_preview)
        print("-" * 40)
        
        print("✅ Notification would be sent to:")
        print("   • Slack: #bug-triage channel")
        print("   • Teams: #qa-alerts channel")
    
    print("\n🎉 Notification feature test completed!")
    print("\n🚀 To use this feature:")
    print("1. Add webhook URLs to your .env file:")
    print("   SLACK_WEBHOOK_URL=https://hooks.slack.com/services/YOUR/WEBHOOK")
    print("   TEAMS_WEBHOOK_URL=https://your-org.webhook.office.com/webhookb2/YOUR/WEBHOOK")
    print("2. Start the Flask application: python app.py")
    print("3. Use the 'Test Log Analysis & Bug Triage' section")
    print("4. Select 'Yes' for Slack or Teams notifications")
    print("5. Click 'Analyze Log' to send notifications automatically")

def get_webhook_setup_instructions():
    """Provide setup instructions for webhooks"""
    
    print("\n🔧 Webhook Setup Instructions:")
    print("=" * 40)
    
    print("\n📱 Slack Setup:")
    print("1. Go to api.slack.com/apps")
    print("2. Create New App > From scratch")
    print("3. Enable 'Incoming Webhooks'")
    print("4. Create webhook for your channel")
    print("5. Copy webhook URL to .env file")
    
    print("\n💼 Teams Setup:")
    print("1. Go to your Teams channel")
    print("2. Click '...' > Connectors")
    print("3. Configure 'Incoming Webhook'")
    print("4. Copy webhook URL to .env file")
    
    print("\n🔑 Environment Variables:")
    print("SLACK_WEBHOOK_URL=https://hooks.slack.com/services/YOUR/SLACK/WEBHOOK")
    print("TEAMS_WEBHOOK_URL=https://your-org.webhook.office.com/webhookb2/YOUR/TEAMS/WEBHOOK")

if __name__ == "__main__":
    test_notification_features()
    get_webhook_setup_instructions() 