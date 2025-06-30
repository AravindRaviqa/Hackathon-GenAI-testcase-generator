# Test Case Generator

A Flask application that generates test cases from user stories using OpenAI's GPT model and integrates with QMetry for test case management.

## Setup

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. Create a `.env` file in the root directory with the following configuration:
```env
# Jira Configuration
JIRA_URL=https://focaloid.atlassian.net
JIRA_EMAIL=your.email@focaloid.com
JIRA_API_TOKEN=your_jira_api_token

# QMetry Configuration
QMETRY_URL=https://focaloid.atlassian.net
QMETRY_API_KEY=your_qmetry_api_key
QMETRY_PROJECT_ID=10000
QMETRY_PROJECT_KEY=QR
QMETRY_API_VERSION=v3

# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key
```

3. Run the application:
```bash
python app.py
```

## Features

- Generate test cases from user stories using AI
- Upload user stories from DOCX, CSV, or XLSX files
- Fetch existing test cases from QMetry
- Create new test cases in QMetry
- Support for multiple test case types:
  - Positive test cases
  - Validation test cases
  - UI/UX test cases
  - Performance test cases
  - Security test cases
  - Combination test cases

## File Formats

The application supports the following file formats:
- DOCX: Text documents containing user stories
- CSV: Spreadsheet files with user stories in a column
- XLSX: Excel files with user stories in a sheet named "Feature List"

## QMetry Integration

The application integrates with QMetry for test case management:
- Fetch existing test cases using QMetry Test Case ID
- Create new test cases in QMetry
- View test case details including steps and expected results

## Environment Variables

The following environment variables are required:

### Jira Configuration
- `JIRA_URL`: Your Jira instance URL (e.g., https://your-domain.atlassian.net)
- `JIRA_EMAIL`: Your Jira account email
- `JIRA_API_TOKEN`: Your Jira API token

### QMetry Configuration
- `QMETRY_URL`: Your QMetry instance URL (usually same as Jira URL)
- `QMETRY_API_KEY`: Your QMetry API key
- `QMETRY_PROJECT_ID`: Your QMetry project ID (numeric)
- `QMETRY_PROJECT_KEY`: Your QMetry project key (e.g., QR)
- `QMETRY_API_VERSION`: QMetry API version (default: v3)

### OpenAI Configuration
- `OPENAI_API_KEY`: Your OpenAI API key

## Security Notes

- Never commit your `.env` file to version control
- Keep your API tokens secure
- Use environment variables for sensitive information 