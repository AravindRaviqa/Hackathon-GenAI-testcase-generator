# Webhook Setup Guide

## Teams Webhook Setup

### Step 1: Create Teams Webhook
1. **Go to your Teams channel** where you want to receive notifications
2. **Click the "..." (three dots)** next to the channel name
3. **Select "Connectors"**
4. **Find "Incoming Webhook"** and click "Configure"
5. **Give it a name** (e.g., "Focaloid GenAI Tools")
6. **Upload an icon** (optional)
7. **Click "Create"**
8. **Copy the webhook URL** - it looks like:
   ```
   https://your-org.webhook.office.com/webhookb2/XXXXXXXXXXXXXXXXXXXXXXXX/IncomingWebhook/XXXXXXXXXXXXXXXXXXXXXXXX/XXXXXXXXXXXXXXXXXXXXXXXX
   ```

### Step 2: Add to .env file
Create a `.env` file in your project root and add:
```
TEAMS_WEBHOOK_URL=https://your-org.webhook.office.com/webhookb2/YOUR/ACTUAL/WEBHOOK/URL
```

## Slack Webhook Setup

### Step 1: Create Slack App
1. **Go to https://api.slack.com/apps**
2. **Click "Create New App"** > "From scratch"
3. **Name your app** (e.g., "Focaloid GenAI Tools")
4. **Select your workspace**
5. **Click "Create App"**

### Step 2: Enable Incoming Webhooks
1. **In your app settings**, go to "Incoming Webhooks"
2. **Toggle "Activate Incoming Webhooks"** to On
3. **Click "Add New Webhook to Workspace"**
4. **Select the channel** where you want notifications
5. **Click "Allow"**
6. **Copy the webhook URL** - it looks like:
   ```
   https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXXXXXX
   ```

### Step 3: Add to .env file
Add to your `.env` file:
```
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/YOUR/ACTUAL/WEBHOOK/URL
```

## Complete .env File Example

```env
# GitHub Configuration
GITHUB_REPO=AravindRaviqa/QuestApp-AI
GITHUB_TOKEN=ghp_your_token_here

# Webhook URLs
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/YOUR/SLACK/WEBHOOK
TEAMS_WEBHOOK_URL=https://your-org.webhook.office.com/webhookb2/YOUR/TEAMS/WEBHOOK

# OpenAI Configuration
OPENAI_API_KEY=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

# Jira Configuration
JIRA_URL=https://aravinddharan.atlassian.net
JIRA_EMAIL=aravind.dharan@gmail.com
JIRA_API_TOKEN=ATATT3xFfGF0r-Q8lM6NxqomQjBtDBjV9GbT7mCMJJNcL37A5gzEFV4NEXba59GZzoL34AYgz1sFHlB_ZgVI6k5ygFlsPykzEATCR_R-n7JwIy_rrM8uST1twosfG4CP0yfiW7y7ph1YN7B0v5nS59w15ubEbeSKVReRJNs1TyGLZccx5XN4x_I=CFBABB3C

# QMetry Configuration
QMETRY_URL=https://aravinddharan.atlassian.net
QMETRY_API_KEY=your_qmetry_api_key_here
QMETRY_PROJECT_ID=your_project_id_here
QMETRY_PROJECT_KEY=your_project_key_here

# Flask Configuration
SECRET_KEY=your_secret_key_here
```

## Testing Your Webhooks

After setting up your webhooks, run the troubleshooting script:

```bash
python troubleshoot_webhooks.py
```

Or test via the web interface:
- Go to `http://localhost:5000/test-webhooks`

## Common Issues

### Teams Webhook Issues:
- **404 Error**: Webhook URL is incorrect or expired
- **403 Error**: Webhook permissions issue
- **Connection Error**: Check internet connection

### Slack Webhook Issues:
- **Invalid URL**: Make sure it starts with `https://hooks.slack.com/services/`
- **Channel not found**: Make sure the webhook is configured for the correct channel

### General Issues:
- **Timeout**: Check your internet connection
- **URL not found**: Verify the webhook URL is correct and active

## Security Notes

- **Never commit your .env file** to version control
- **Keep webhook URLs private** - they provide access to your channels
- **Rotate webhook URLs** periodically for security
- **Use environment-specific webhooks** for different environments (dev/staging/prod) 