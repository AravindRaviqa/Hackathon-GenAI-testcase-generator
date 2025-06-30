from flask import Flask, render_template, request, jsonify, flash, send_file
from flask_wtf import FlaskForm, CSRFProtect
from flask_wtf.file import FileField, FileAllowed
from wtforms import TextAreaField, SubmitField, StringField
from wtforms.validators import Optional
from openai import OpenAI
from dotenv import load_dotenv
import os
import pandas as pd
from docx import Document
import io
import re
import requests
from requests.auth import HTTPBasicAuth
import json
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from jira import JIRA
import time

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', os.urandom(24))  # Use environment variable if available
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
csrf = CSRFProtect(app)

# Configure OpenAI
openai_api_key = "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"
client = OpenAI(api_key=openai_api_key)

# Initialize QMetry connection
QMETRY_CONFIG = {
    'url': os.getenv('QMETRY_URL'),
    'api_key': os.getenv('QMETRY_API_KEY'),
    'project_id': os.getenv('QMETRY_PROJECT_ID'),
    'project_key': os.getenv('QMETRY_PROJECT_KEY'),
    'headers': {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'X-QMetry-API-Key': os.getenv('QMETRY_API_KEY'),
        'X-QMetry-Project-Key': os.getenv('QMETRY_PROJECT_KEY')
    }
}

# Validate QMetry configuration
if not all([QMETRY_CONFIG['api_key'], QMETRY_CONFIG['project_id'], QMETRY_CONFIG['project_key']]):
    raise ValueError("Required QMetry environment variables are not set")

# Jira Configuration
JIRA_CONFIG = {
    'url': os.getenv('JIRA_URL'),
    'email': os.getenv('JIRA_EMAIL'),
    'api_token': os.getenv('JIRA_API_TOKEN')
}

# Validate Jira configuration
if not JIRA_CONFIG['api_token']:
    raise ValueError("JIRA_API_TOKEN environment variable is not set")

# Add custom nl2br filter
@app.template_filter('nl2br')
def nl2br_filter(s):
    if not s:
        return ""
    return s.replace('\n', '<br>')

class UserStoryForm(FlaskForm):
    user_story = TextAreaField('User Story', validators=[Optional()])
    jira_id = StringField('Jira Ticket ID', validators=[Optional()])
    qmetry_id = StringField('QMetry ID', validators=[Optional()])
    file = FileField('Upload Document/CSV', validators=[
        Optional(),
        FileAllowed(['docx', 'csv', 'xlsx'], 'Only .docx, .csv, and .xlsx files are allowed!')
    ])
    submit = SubmitField('Generate Test Cases')

class JiraTestCaseGenerator:
    def __init__(self):
        self.jira = None
        self.qmetry = None
        self.jira_url = JIRA_CONFIG['url']
        self.jira_email = JIRA_CONFIG['email']
        self.jira_api_token = JIRA_CONFIG['api_token']
        
        # Load QMetry credentials
        self.qmetry_api_key = QMETRY_CONFIG['api_key']
        self.qmetry_project_id = QMETRY_CONFIG['project_id']
        self.qmetry_project_key = QMETRY_CONFIG['project_key']
        self.qmetry_url = self.jira_url
        
        try:
            # Create a session with proper headers
            session = requests.Session()
            session.headers.update({
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'X-Atlassian-Token': 'no-check'
            })
            
            # Try to authenticate with the session
            auth_url = f"{self.jira_url}/rest/api/2/myself"
            response = session.get(
                auth_url,
                auth=(self.jira_email, self.jira_api_token),
                verify=True
            )
            
            if response.status_code == 200:
                # If authentication successful, create JIRA instance
                self.jira = JIRA(
                    server=self.jira_url,
                    basic_auth=(self.jira_email, self.jira_api_token),
                    validate=True,
                    options={
                        'verify': True,
                        'headers': {
                            'X-Atlassian-Token': 'no-check'
                        }
                    }
                )
                
                # Initialize QMetry connection
                if self.qmetry_api_key:
                    self.qmetry = {
                        'url': self.qmetry_url,
                        'headers': {
                            'Accept': 'application/json',
                            'Content-Type': 'application/json',
                            'X-QMetry-API-Key': self.qmetry_api_key,
                            'X-QMetry-Project-Key': self.qmetry_project_key
                        },
                        'project_id': self.qmetry_project_id,
                        'project_key': self.qmetry_project_key
                    }
        except Exception as e:
            flash(f"Failed to connect to Jira: {str(e)}")

    def get_jira_ticket(self, ticket_id):
        if not self.jira:
            flash("Jira connection not configured. Please check your .env file.")
            return None
        
        try:
            # Clean the ticket ID
            ticket_id = ticket_id.strip()
            
            # Try to fetch the issue with retry logic
            max_retries = 3
            retry_count = 0
            
            while retry_count < max_retries:
                try:
                    if retry_count > 0:
                        time.sleep(2)
                        
                    issue = self.jira.issue(ticket_id)
                    if issue:
                        return {
                            'key': issue.key,
                            'summary': issue.fields.summary,
                            'description': issue.fields.description
                        }
                    break
                except Exception as e:
                    retry_count += 1
                    if retry_count == max_retries:
                        raise e
                    flash(f"Retry {retry_count} of {max_retries}...")
            
            flash(f"Could not find Jira ticket: {ticket_id}")
            return None
                
        except Exception as e:
            flash(f"Error fetching Jira ticket: {str(e)}")
            return None

    def extract_requirements(self, description):
        if not description:
            return []
            
        # Clean up the description
        description = re.sub(r'<[^>]+>', '', description)  # Remove HTML tags
        description = description.replace('{panel}', '').replace('{/panel}', '')  # Remove Jira panels
        
        # Split into lines and clean
        lines = [line.strip() for line in description.split('\n') if line.strip()]
        
        # Remove markdown-style formatting
        lines = [line.lstrip('#').lstrip('*').lstrip('-').lstrip(' ').strip() for line in lines]
        
        # If no clear requirements found, use the entire description
        if not lines:
            return [description.strip()]
            
        return lines

    def generate_test_case(self, requirement, tc_id):
        # Generate steps based on requirement
        steps = []
        requirement_lower = requirement.lower()
        
        # Extract action from requirement
        action = None
        if 'verify' in requirement_lower:
            action = requirement.split('verify')[1].strip()
        elif 'should' in requirement_lower:
            action = requirement.split('should')[1].strip()
        elif 'must' in requirement_lower:
            action = requirement.split('must')[1].strip()
        else:
            action = requirement
            
        # Generate steps
        steps.append(f"1. Access the system")
        steps.append(f"2. Navigate to the relevant section")
        steps.append(f"3. Perform {action}")
        steps.append(f"4. Verify the system's response")
        
        return {
            'Test Case ID': f'TC_{tc_id:03d}',
            'Summary': f"Verify {action[:100]}...",
            'Type': 'Functional',
            'Priority': 'High',
            'Steps': '\n'.join(steps),
            'Expected Result': f"The system should successfully handle {action[:100]}..."
        }

    def generate_test_cases(self, requirements):
        test_cases = []
        tc_id = 1
        
        for requirement in requirements:
            if len(requirement) < 5:  # Skip very short requirements
                continue
                
            test_case = self.generate_test_case(requirement, tc_id)
            test_cases.append(test_case)
            tc_id += 1
            
        return pd.DataFrame(test_cases)

    def generate_pdf(self, test_cases_df, ticket_id):
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        styles = getSampleStyleSheet()
        story = []

        # Title
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=16,
            spaceAfter=30
        )
        story.append(Paragraph(f"Test Cases for {ticket_id}", title_style))
        story.append(Spacer(1, 12))

        # Process each test case
        for _, row in test_cases_df.iterrows():
            story.append(Paragraph(f"Test Case {row['Test Case ID']}", styles['Heading2']))
            story.append(Paragraph(f"Summary: {row['Summary']}", styles['Normal']))
            story.append(Spacer(1, 12))

            story.append(Paragraph(f"Type: {row['Type']}", styles['Normal']))
            story.append(Paragraph(f"Priority: {row['Priority']}", styles['Normal']))
            story.append(Spacer(1, 12))

            story.append(Paragraph("Steps:", styles['Heading3']))
            steps = row['Steps'].split('\n')
            for step in steps:
                story.append(Paragraph(step, styles['Normal']))
            story.append(Spacer(1, 12))

            story.append(Paragraph("Expected Result:", styles['Heading3']))
            story.append(Paragraph(row['Expected Result'], styles['Normal']))
            story.append(Spacer(1, 20))

        doc.build(story)
        buffer.seek(0)
        return buffer.getvalue()

    def create_qmetry_folder(self, ticket_id):
        if not self.qmetry:
            flash("QMetry connection not configured. Please check your credentials.")
            return None
            
        try:
            folder_name = ticket_id
            folder_url = f"{self.jira_url}/plugins/servlet/ac/com.infostretch.QmetryTestManager/qtm4j-test-management/api/folders"
            
            auth = (self.jira_email, self.jira_api_token)
            headers = {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'X-QMetry-API-Key': self.qmetry_api_key,
                'X-QMetry-Project-Key': self.qmetry_project_key,
                'X-Atlassian-Token': 'no-check'
            }
            
            payload = {
                "name": folder_name,
                "projectId": self.qmetry_project_id,
                "parentId": -1,
                "type": "TEST_CASE"
            }
            
            session = requests.Session()
            session.headers.update(headers)
            
            csrf_url = f"{self.jira_url}/rest/api/2/myself"
            csrf_response = session.get(csrf_url, auth=auth, verify=True)
            if csrf_response.status_code != 200:
                flash(f"Failed to authenticate with Jira: {csrf_response.status_code}")
                return None
            
            response = session.post(
                folder_url,
                auth=auth,
                json=payload,
                verify=True
            )
            
            if response.status_code in [200, 201]:
                try:
                    result = response.json()
                    flash(f"New Folder created: {folder_name}")
                    return result.get('id')
                except json.JSONDecodeError as e:
                    flash(f"Invalid JSON response: {str(e)}\nResponse content: {response.text}")
                    return None
            else:
                error_message = f"Failed to create folder: {folder_name}. Status code: {response.status_code}"
                try:
                    error_json = response.json()
                    error_message += f"\nError details: {json.dumps(error_json, indent=2)}"
                except json.JSONDecodeError:
                    error_message += f"\nResponse content: {response.text}"
                flash(error_message)
                return None
                
        except Exception as e:
            flash(f"Error creating folder: {str(e)}")
            return None

    def upload_to_qmetry(self, test_cases_df, ticket_id):
        if not self.qmetry:
            flash("QMetry connection not configured. Please check your credentials.")
            return False
            
        try:
            folder_id = self.create_qmetry_folder(ticket_id)
            if not folder_id:
                return False
            
            # Process test cases in smaller chunks
            chunk_size = 5  # Process 5 test cases at a time
            test_cases = []
            success_count = 0
            failed_count = 0
            
            for _, row in test_cases_df.iterrows():
                steps_list = row['Steps'].split('\n')
                formatted_steps = []
                
                for i, step in enumerate(steps_list, 1):
                    if step.strip():
                        formatted_steps.append({
                            "stepDetails": step.strip(),
                            "expectedResult": row['Expected Result'],
                            "id": i,
                            "isChecked": False,
                            "isExpanded": True
                        })
                
                test_case = {
                    "summary": row['Summary'][:255],  # Limit summary length
                    "description": row['Steps'][:1000],  # Limit description length
                    "precondition": row['Expected Result'][:1000],  # Limit precondition length
                    "folderId": str(folder_id),
                    "priority": "Medium",
                    "status": "Draft",
                    "type": "Functional",
                    "projectId": self.qmetry_project_id,
                    "projectKey": self.qmetry_project_key,
                    "steps": formatted_steps
                }
                test_cases.append(test_case)
                
                # Process in chunks
                if len(test_cases) >= chunk_size:
                    success, failed = self._process_test_case_chunk(test_cases)
                    success_count += success
                    failed_count += failed
                    test_cases = []  # Clear the chunk
            
            # Process any remaining test cases
            if test_cases:
                success, failed = self._process_test_case_chunk(test_cases)
                success_count += success
                failed_count += failed
            
            if success_count > 0:
                flash(f"Test cases added successfully to the folder {ticket_id}")
            if failed_count > 0:
                flash(f"Failed to add {failed_count} test cases")
            
            return success_count > 0
                
        except Exception as e:
            flash(f"Error creating test cases in QMetry: {str(e)}")
            return False
            
    def _process_test_case_chunk(self, test_cases):
        """Process a chunk of test cases and return success/failure counts"""
        success_count = 0
        failed_count = 0
        
        create_url = f"{self.jira_url}/rest/qtm4j/1.0/testcase"
        
        # Create a session with proper headers and authentication
        session = requests.Session()
        session.headers.update({
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'X-QMetry-API-Key': self.qmetry_api_key,
            'X-QMetry-Project-Key': self.qmetry_project_key,
            'X-Atlassian-Token': 'no-check'
        })
        
        for test_case in test_cases:
            try:
                response = session.post(
                    create_url,
                    auth=(self.jira_email, self.jira_api_token),
                    json=test_case,
                    verify=True
                )
                
                if response.status_code in [200, 201]:
                    success_count += 1
                else:
                    error_message = f"Failed to create test case. Status code: {response.status_code}"
                    try:
                        error_json = response.json()
                        error_message += f"\nError details: {json.dumps(error_json, indent=2)}"
                    except json.JSONDecodeError:
                        error_message += f"\nResponse content: {response.text}"
                    flash(error_message)
                    failed_count += 1
                    
            except Exception as e:
                flash(f"Error creating test case: {str(e)}")
                failed_count += 1
                
        return success_count, failed_count

    def generate_pdf_for_user_stories(self, structured_test_cases, title):
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        styles = getSampleStyleSheet()
        story = []

        # Title
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=16,
            spaceAfter=30
        )
        story.append(Paragraph(f"Test Cases - {title}", title_style))
        story.append(Spacer(1, 12))

        # Process each user story and its test cases
        for i, case in enumerate(structured_test_cases, 1):
            # User Story
            story.append(Paragraph(f"User Story {i}", styles['Heading2']))
            story.append(Paragraph(case['user_story'], styles['Normal']))
            story.append(Spacer(1, 12))

            # Test Cases for this user story
            story.append(Paragraph("Test Cases:", styles['Heading3']))
            for j, test_case in enumerate(case['test_cases'], 1):
                story.append(Paragraph(f"Test Case {j}:", styles['Heading4']))
                story.append(Paragraph(test_case, styles['Normal']))
                story.append(Spacer(1, 12))

            story.append(Spacer(1, 20))

        doc.build(story)
        buffer.seek(0)
        return buffer.getvalue()

def extract_text_from_docx(file):
    doc = Document(file)
    return '\n'.join([paragraph.text for paragraph in doc.paragraphs])

def extract_user_stories_from_csv(file):
    df = pd.read_csv(file)
    if 'User story' in df.columns:
        return df['User story'].dropna().tolist()
    elif len(df.columns) >= 3:
        flash(f"Column 'User story' not found. Available columns: {', '.join(df.columns)}. Using column C as fallback.")
        return df.iloc[:, 2].dropna().tolist()
    else:
        flash(f"No suitable 'User story' column found. Available columns: {', '.join(df.columns)}")
        return []

def extract_user_stories_from_xlsx(file):
    xl = pd.ExcelFile(file)
    # Find the sheet name case-insensitively
    sheet_name = None
    for s in xl.sheet_names:
        if s.strip().lower() == 'feature list':
            sheet_name = s
            break
    if not sheet_name:
        flash(f"Sheet 'Feature List' not found. Available sheets: {', '.join(xl.sheet_names)}")
        return []
    df = xl.parse(sheet_name)
    # Try to get 'User story' column by header, else fallback to column C
    if 'User story' in df.columns:
        return df['User story'].dropna().tolist()
    elif len(df.columns) >= 3:
        flash(f"Column 'User story' not found. Available columns: {', '.join(df.columns)}. Using column C as fallback.")
        return df.iloc[:, 2].dropna().tolist()
    else:
        flash(f"No suitable 'User story' column found. Available columns: {', '.join(df.columns)}")
        return []

def fetch_qmetry_story(qmetry_id):
    try:
        session = requests.Session()
        
        # Jira Authentication Test
        auth_url = "https://aravinddharan.atlassian.net/rest/api/3/myself"
        auth = HTTPBasicAuth("aravind.dharan@gmail.com", "ATATT3xFfGF0r-Q8lM6NxqomQjBtDBjV9GbT7mCMJJNcL37A5gzEFV4NEXba59GZzoL34AYgz1sFHlB_ZgVI6k5ygFlsPykzEATCR_R-n7JwIy_rrM8uST1twosfG4CP0yfiW7y7ph1YN7B0v5nS59w15ubEbeSKVReRJNs1TyGLZccx5XN4x_I=CFBABB3C")
        response = session.get(auth_url, auth=HTTPBasicAuth(JIRA_CONFIG['email'], JIRA_CONFIG['api_token']))
        if response.status_code != 200:
            return f"Jira authentication failed: {response.status_code} - {response.text}"

        # QMetry Fetch Test Case
        base_url = JIRA_CONFIG['url'].rstrip('/')
        url = f"{base_url}/rest/qtm4j/2.0/testcase/{qmetry_id}"

        headers = QMETRY_CONFIG['headers']
        response = requests.get(url, headers=headers, auth=auth)
        
        if response.status_code == 200:
            return response.json()
        else:
            return f"Error fetching test case: {response.status_code} - {response.text}"

    except Exception as e:
        return f"Error: {str(e)}"

def create_qmetry_test_case(test_case_data):
    try:
        session = requests.Session()
        
        # QMetry Create Test Case
        base_url = JIRA_CONFIG['url'].rstrip('/')
        url = f"{base_url}/rest/qtm4j/1.0/testcase"

        # Set up authentication and headers
        auth = HTTPBasicAuth(JIRA_CONFIG['email'], JIRA_CONFIG['api_token'])
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'X-QMetry-API-Key': QMETRY_CONFIG['api_key'],
            'X-QMetry-Project-Key': QMETRY_CONFIG['project_key']
        }

        # Add required fields for QTM4J
        test_case_data.update({
            'projectId': QMETRY_CONFIG['project_id'],
            'projectKey': QMETRY_CONFIG['project_key'],
            'type': 'Functional',  # Required field
            'status': 'Draft',     # Required field
            'priority': 'Medium'   # Required field
        })

        print(f"Requesting URL: {url}")
        print(f"Request headers: {headers}")
        print(f"Request data: {json.dumps(test_case_data, indent=2)}")

        # Make the request with authentication
        response = session.post(url, headers=headers, json=test_case_data, auth=auth)
        print(f"Response status: {response.status_code}")
        print(f"Response headers: {dict(response.headers)}")
        print(f"Response content: {response.text}")

        try:
            if response.status_code in [200, 201]:
                response_json = response.json()
                return {'success': True, 'message': 'Test case created', 'response': response_json}
            else:
                # Try to parse error response as JSON
                try:
                    error_json = response.json()
                    error_message = error_json.get('message', response.text)
                except json.JSONDecodeError:
                    error_message = response.text
                return {'success': False, 'message': f"QMetry error {response.status_code}: {error_message}"}
        except json.JSONDecodeError as e:
            return {'success': False, 'message': f"Invalid JSON response from QMetry: {str(e)}\nResponse content: {response.text}"}

    except Exception as e:
        return {'success': False, 'message': f"Error creating test case: {str(e)}"}

def generate_test_cases(user_story):
    try:
        if not client:
            return "Error: OpenAI client not initialized. Please check your API key."

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a QA expert. Generate detailed test cases from the given user story. For each user story, include: Positive test cases, Validation (negative/edge case) test cases, UI/UX test cases, Performance test cases, Security test cases, and all possible combination test cases. For each test case, provide: test case ID, description, preconditions, steps, expected results, and priority. Clearly separate positive, validation, UI/UX, performance, security, and combination test cases."},
                {"role": "user", "content": f"Generate test cases for this user story:\n\n{user_story}"}
            ],
            temperature=0.7,
            max_tokens=2000
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error generating test cases: {str(e)}"

def parse_test_cases(ai_output):
    # Split by test case (simple heuristic: look for 'Test Case' or 'TC' at the start of a line)
    cases = re.split(r'\n(?=Test Case|TC\d+)', ai_output)
    parsed = []
    for case in cases:
        if case.strip():
            parsed.append(case.strip())
    return parsed

@app.route('/', methods=['GET', 'POST'])
def index():
    form = UserStoryForm()
    test_cases = None
    structured_test_cases = None
    jira_ticket = None
    pdf_path = None
    excel_path = None
    
    if form.validate_on_submit():
        # Handle Jira ticket ID
        if form.jira_id.data:
            generator = JiraTestCaseGenerator()
            jira_ticket = generator.get_jira_ticket(form.jira_id.data)
            
            if jira_ticket:
                requirements = generator.extract_requirements(jira_ticket['description'])
                test_cases_df = generator.generate_test_cases(requirements)
                
                if not test_cases_df.empty:
                    # Generate PDF
                    pdf_data = generator.generate_pdf(test_cases_df, jira_ticket['key'])
                    
                    # Save PDF to a temporary file
                    pdf_path = f"static/temp/{jira_ticket['key']}_test_cases.pdf"
                    os.makedirs(os.path.dirname(pdf_path), exist_ok=True)
                    with open(pdf_path, 'wb') as f:
                        f.write(pdf_data)
                    
                    # Save Excel
                    excel_path = f"static/temp/{jira_ticket['key']}_test_cases.xlsx"
                    test_cases_df.to_excel(excel_path, index=False)
                    
                    return render_template('index.html', 
                                        form=form,
                                        jira_ticket=jira_ticket,
                                        test_cases_df=test_cases_df,
                                        pdf_path=pdf_path,
                                        excel_path=excel_path)
                else:
                    flash("No test cases could be generated from the ticket description.")
        
        # Handle file upload
        if form.file.data:
            file = form.file.data
            filename = file.filename.lower()
            user_stories = []
            if filename.endswith('.docx'):
                user_story = extract_text_from_docx(file)
                user_stories = [user_story]  # Convert single story to list for consistency
            elif filename.endswith('.csv'):
                user_stories = extract_user_stories_from_csv(file)
            elif filename.endswith('.xlsx'):
                user_stories = extract_user_stories_from_xlsx(file)
            if user_stories:
                structured_test_cases = []
                for idx, us in enumerate(user_stories, 1):
                    tc = generate_test_cases(us)
                    parsed = parse_test_cases(tc)
                    structured_test_cases.append({
                        'user_story': us,
                        'test_cases': parsed
                    })
                
                # Generate export files for file uploads
                if structured_test_cases:
                    generator = JiraTestCaseGenerator()
                    
                    # Generate PDF using the new method
                    pdf_data = generator.generate_pdf_for_user_stories(structured_test_cases, f"Uploaded File: {filename}")
                    
                    # Save PDF to a temporary file
                    pdf_path = f"static/temp/uploaded_{filename.split('.')[0]}_test_cases.pdf"
                    os.makedirs(os.path.dirname(pdf_path), exist_ok=True)
                    with open(pdf_path, 'wb') as f:
                        f.write(pdf_data)
                    
                    # Create Excel file with combined test cases
                    export_test_cases = []
                    for case in structured_test_cases:
                        for test_case in case['test_cases']:
                            export_test_cases.append({
                                'User Story': case['user_story'][:100] + '...' if len(case['user_story']) > 100 else case['user_story'],
                                'Test Case': test_case
                            })
                    
                    if export_test_cases:
                        test_cases_df = pd.DataFrame(export_test_cases)
                        # Save Excel
                        excel_path = f"static/temp/uploaded_{filename.split('.')[0]}_test_cases.xlsx"
                        test_cases_df.to_excel(excel_path, index=False)
                
                return render_template('index.html', form=form, structured_test_cases=structured_test_cases, pdf_path=pdf_path, excel_path=excel_path)
        
        # Handle QMetry ID
        if form.qmetry_id.data:
            qmetry_story = fetch_qmetry_story(form.qmetry_id.data)
            if form.user_story.data:
                user_story = f"{form.user_story.data}\n\nQMetry Test Case:\n{qmetry_story}"
            else:
                user_story = qmetry_story
        
        if form.user_story.data:
            tc = generate_test_cases(form.user_story.data)
            parsed = parse_test_cases(tc)
            structured_test_cases = [{
                'user_story': form.user_story.data,
                'test_cases': parsed
            }]
            
            # Generate export files for user stories
            if structured_test_cases:
                generator = JiraTestCaseGenerator()
                
                # Generate PDF using the new method
                pdf_data = generator.generate_pdf_for_user_stories(structured_test_cases, "User Story Test Cases")
                
                # Save PDF to a temporary file
                pdf_path = f"static/temp/user_story_test_cases.pdf"
                os.makedirs(os.path.dirname(pdf_path), exist_ok=True)
                with open(pdf_path, 'wb') as f:
                    f.write(pdf_data)
                
                # Create Excel file with combined test cases
                export_test_cases = []
                for case in structured_test_cases:
                    for test_case in case['test_cases']:
                        export_test_cases.append({
                            'User Story': case['user_story'][:100] + '...' if len(case['user_story']) > 100 else case['user_story'],
                            'Test Case': test_case
                        })
                
                if export_test_cases:
                    test_cases_df = pd.DataFrame(export_test_cases)
                    # Save Excel
                    excel_path = f"static/temp/user_story_test_cases.xlsx"
                    test_cases_df.to_excel(excel_path, index=False)
            
            # Create test cases in QMetry
            for test_case in parsed:
                test_case_data = {
                    'name': test_case.split('\n')[0],
                    'description': test_case,
                    'priority': 'Medium',
                    'status': 'Draft',
                    'type': 'Functional',
                    'steps': [{
                        'stepNumber': 1,
                        'step': test_case,
                        'expectedResult': 'Test case executed successfully'
                    }],
                    'projectKey': QMETRY_CONFIG['project_key'],
                    'projectId': QMETRY_CONFIG['project_id']
                }
                response = create_qmetry_test_case(test_case_data)
                if not response['success']:
                    flash(f"Warning: {response['message']}")
    
    return render_template('index.html', form=form, structured_test_cases=structured_test_cases, jira_ticket=jira_ticket, pdf_path=pdf_path, excel_path=excel_path)

@app.route('/download/<path:filename>')
def download_file(filename):
    return send_file(filename, as_attachment=True)

@csrf.exempt
@app.route('/add-to-qmetry', methods=['POST'])
def add_to_qmetry():
    try:
        if not request.is_json:
            return jsonify({'success': False, 'message': 'Request must be JSON'}), 400

        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'message': 'No data provided'}), 400

        test_cases = data.get('test_cases', [])
        ticket_id = data.get('ticket_id')
        
        if not test_cases:
            return jsonify({'success': False, 'message': 'No test cases provided'}), 400
        if not ticket_id:
            return jsonify({'success': False, 'message': 'No ticket ID provided'}), 400

        generator = JiraTestCaseGenerator()
        if not generator.jira:
            return jsonify({'success': False, 'message': 'Jira connection not configured'}), 500

        # Limit the data size by only sending necessary fields
        test_cases_df = pd.DataFrame(test_cases)
        test_cases_df = test_cases_df[['Test Case ID', 'Summary', 'Type', 'Priority', 'Steps', 'Expected Result']]
        
        try:
            if generator.upload_to_qmetry(test_cases_df, ticket_id):
                return jsonify({'success': True, 'message': 'Test cases added to QMetry successfully'})
            else:
                return jsonify({'success': False, 'message': 'Failed to add test cases to QMetry'}), 500
        except requests.exceptions.RequestException as e:
            app.logger.error(f"Network error in upload_to_qmetry: {str(e)}")
            return jsonify({'success': False, 'message': f'Network error: {str(e)}'}), 503
        except Exception as e:
            app.logger.error(f"Error in upload_to_qmetry: {str(e)}")
            return jsonify({'success': False, 'message': f'Error uploading to QMetry: {str(e)}'}), 500
    
    except Exception as e:
        app.logger.error(f"Error in add_to_qmetry: {str(e)}")
        return jsonify({'success': False, 'message': str(e)}), 500

# Configure CSRF protection
@app.after_request
def add_csrf_header(response):
    if 'X-CSRFToken' not in response.headers:
        response.headers['X-CSRFToken'] = csrf._get_csrf_token()
    return response

if __name__ == '__main__':
    app.run(debug=True) 


