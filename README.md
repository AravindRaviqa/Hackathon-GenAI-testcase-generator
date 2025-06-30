# Focaloid GenAI-Powered Quality Engineering Tools

A powerful AI-driven test case generation tool that transforms user stories, Jira tickets, and natural language descriptions into comprehensive test cases and automation scripts.

## 🚀 Features

### Core Features
- **User Story to Test Cases**: Convert user stories into detailed test cases using AI
- **Jira Integration**: Extract requirements from Jira tickets and generate test cases
- **Document Processing**: Upload and process .docx, .csv, and .xlsx files
- **QMetry Integration**: Export test cases directly to QMetry test management
- **Export Options**: Download test cases as PDF or Excel files

### 🤖 NEW: Natural Language to Automation Script
- **Plain English to Code**: Convert natural language test scenarios into working automation scripts
- **Multiple Frameworks**: Support for Selenium and Playwright in both Python and JavaScript
- **Smart Code Generation**: AI-powered script generation with best practices
- **Download & Copy**: Download generated scripts or copy to clipboard
- **Validation & Screenshots**: Includes error handling and screenshot capture logic

## 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Hackathon-GenAI-testcase-generator
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   Create a `.env` file in the root directory:
   ```env
   SECRET_KEY=your_secret_key_here
   OPENAI_API_KEY=your_openai_api_key
   JIRA_URL=https://your-domain.atlassian.net
   JIRA_EMAIL=your_email@domain.com
   JIRA_API_TOKEN=your_jira_api_token
   QMETRY_URL=https://your-domain.atlassian.net
   QMETRY_API_KEY=your_qmetry_api_key
   QMETRY_PROJECT_ID=your_project_id
   QMETRY_PROJECT_KEY=your_project_key
   ```

5. **Run the application**
   ```bash
   python app.py
   ```

## 📖 Usage

### Test Case Generation

1. **From User Story**: Enter a user story in the text area and click "Generate Test Cases"
2. **From Jira Ticket**: Enter a Jira ticket ID (e.g., MBA-4) to extract requirements
3. **From Document**: Upload a .docx, .csv, or .xlsx file containing user stories
4. **Export**: Download generated test cases as PDF or Excel files

### 🤖 Automation Script Generation

1. **Enter Scenario**: Describe your test scenario in plain English
   ```
   Example: "Login with valid credentials and check dashboard"
   Example: "Navigate to product page, add item to cart, and verify checkout process"
   ```

2. **Choose Framework**: Select your preferred automation framework:
   - Selenium (Python)
   - Selenium (JavaScript)
   - Playwright (Python)
   - Playwright (JavaScript)

3. **Generate Script**: Click "Generate Automation Script" to create working code

4. **Download/Copy**: Download the script file or copy the code to clipboard

### Example Automation Scenarios

#### Simple Login Test
```
Input: "Login with valid credentials and check dashboard"
Output: Complete Selenium/Playwright script with:
- WebDriver setup and teardown
- Login form interaction
- Dashboard verification
- Screenshot capture on failure
- Error handling
```

#### E-commerce Flow
```
Input: "Navigate to product page, add item to cart, and verify checkout process"
Output: Complete automation script with:
- Product page navigation
- Add to cart functionality
- Checkout process validation
- Form filling and submission
- Order confirmation verification
```

## 🔧 Supported Frameworks

### Selenium (Python)
- WebDriver setup with Chrome/Firefox
- Explicit waits and element locators
- Screenshot capture on failure
- Page Object Model structure
- Error handling and logging

### Selenium (JavaScript)
- WebDriver setup with Node.js
- Async/await patterns
- Explicit waits and element locators
- Screenshot capture on failure
- Error handling and logging

### Playwright (Python)
- Browser setup and teardown
- Modern element locators
- Built-in assertions
- Screenshot and video capture
- Error handling and logging

### Playwright (JavaScript)
- Browser setup and teardown
- Modern element locators
- Built-in assertions
- Screenshot and video capture
- Error handling and logging

## 📁 Project Structure

```
Hackathon-GenAI-testcase-generator/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── README.md             # Project documentation
├── static/               # Static files
│   ├── js/
│   │   └── main.js       # JavaScript functionality
│   ├── temp/             # Generated files
│   └── ...               # Other static assets
└── templates/
    └── index.html        # Main application template
```

## 🔑 API Keys Required

- **OpenAI API Key**: For AI-powered test case and script generation
- **GitHub Personal Access Token**: For assignee suggestions based on commit history (optional)
- **Jira API Token**: For Jira ticket integration (optional)
- **QMetry API Key**: For QMetry test management integration (optional)

### Optional Integrations

The following integrations are optional and only required if you want to use specific features:

- **Jira Integration**: Only needed for extracting requirements from Jira tickets
- **QMetry Integration**: Only needed for exporting test cases to QMetry
- **GitHub Integration**: Only needed for suggesting assignees based on commit history

If these integrations are not configured, the application will still work for:
- Test case generation from user stories
- Automation script generation
- Log analysis and bug triage (without assignee suggestions)

## 🚀 Benefits

### For Manual Testers
- **No Coding Required**: Generate automation scripts from plain English
- **Faster Adoption**: Bridge the gap between manual and automated testing
- **Learning Tool**: Study generated code to learn automation practices

### For Automation Engineers
- **Rapid Prototyping**: Quickly generate script templates
- **Best Practices**: AI-generated code follows industry standards
- **Time Savings**: Focus on customization rather than boilerplate code

### For Teams
- **Consistency**: Standardized automation patterns across the team
- **Documentation**: Natural language scenarios serve as living documentation
- **Maintenance**: Easier to understand and maintain AI-generated code

## 🎯 Impact

- **Reduces Automation Barrier**: Helps manual testers contribute to automation
- **Speeds Up Scripting**: 80% faster script generation
- **Improves Quality**: Consistent, well-structured automation code
- **Enhances Collaboration**: Shared understanding through natural language

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Create an issue in the repository
- Contact the development team
- Check the documentation for common solutions 