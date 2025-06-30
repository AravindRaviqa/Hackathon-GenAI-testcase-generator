#!/usr/bin/env python3
"""
Test script to demonstrate the enhanced Bug Assignment Recommendation feature
"""

def test_bug_assignment_analysis():
    """Test the enhanced bug assignment analysis functionality"""
    
    # Sample test failure logs
    test_logs = [
        {
            "name": "Frontend UI Test Failure",
            "log": """
[ERROR] Test failed: LoginPage.test_user_login
AssertionError: Expected element with id 'dashboard-welcome' to be visible
File: /src/components/LoginPage.js
Line: 45: expect(driver.findElement(By.id('dashboard-welcome')).isDisplayed()).toBe(true);
Stack trace: LoginPage.js:45: LoginPage.test_user_login
            """,
            "expected_assignee_type": "Frontend Developer"
        },
        {
            "name": "API Integration Test Failure", 
            "log": """
[ERROR] Test failed: UserService.test_create_user
HTTPError: 500 Internal Server Error
POST /api/users
Response: {"error": "Database connection failed", "details": "Connection timeout"}
File: /src/services/UserService.java
Line: 123: User user = userRepository.save(userRequest);
Stack trace: UserService.java:123: UserService.test_create_user
            """,
            "expected_assignee_type": "Backend Developer"
        },
        {
            "name": "CI/CD Pipeline Failure",
            "log": """
[ERROR] Build failed: Jenkins pipeline stage 'deploy-to-staging'
Exception: Docker build failed
Error: Failed to build image: no space left on device
File: /Jenkinsfile
Line: 15: docker build -t myapp:latest .
Stack trace: Jenkinsfile:15: deploy-to-staging
            """,
            "expected_assignee_type": "DevOps Engineer"
        }
    ]
    
    print("🧠 Testing Enhanced Bug Assignment Recommendation Feature")
    print("=" * 70)
    
    for i, test in enumerate(test_logs, 1):
        print(f"\n📝 Test Case {i}: {test['name']}")
        print(f"🎯 Expected Assignee Type: {test['expected_assignee_type']}")
        print("🔄 Analyzing log for bug assignment...")
        
        # Simulate the AI analysis process
        print("📄 AI Analysis Preview:")
        print("-" * 50)
        
        # Simulate the enhanced analysis output
        analysis_output = f"""
**Failure Summary**: {test['name']}
**Root Cause Analysis**: {get_root_cause_analysis(test['log'])}
**Affected Components**: {get_affected_components(test['log'])}
**Severity Assessment**: {get_severity_assessment(test['log'])}
**Recommended Assignee Type**: {test['expected_assignee_type']}

🔍 **GitHub-Based Assignee Suggestions** (from recent commit history):
📁 {get_affected_components(test['log'])}: John Developer (@johndev) 🔴

💡 **Assignment Strategy**:
• 🎯 **Primary Expert**: John Developer (@johndev) - 8 recent commits
• 👥 **Team Involvement**: 3 contributors involved in affected files
• 🔄 **Moderate Activity**: Recent contributor should be able to handle this
• 📊 **Consider Workload**: Check current sprint capacity before assignment
• 🚨 **Critical Issues**: Consider escalation to senior team members
"""
        
        print(analysis_output)
        print("-" * 50)
        
    print("\n🎉 Enhanced bug assignment analysis test completed!")
    print("\n🚀 To use this feature:")
    print("1. Start the Flask application: python app.py")
    print("2. Open your browser to http://localhost:5000")
    print("3. Scroll to the 'Test Log Analysis & Bug Triage' section")
    print("4. Paste a test failure log and click 'Analyze Log'")
    print("5. View the AI-generated assignment recommendations")

def get_root_cause_analysis(log):
    """Simulate root cause analysis based on log content"""
    if "UI" in log or "element" in log:
        return "Frontend rendering issue or element visibility problem"
    elif "API" in log or "HTTP" in log or "Database" in log:
        return "Backend service or database connectivity issue"
    elif "Jenkins" in log or "Docker" in log or "pipeline" in log:
        return "CI/CD infrastructure or deployment configuration issue"
    else:
        return "General application error requiring investigation"

def get_affected_components(log):
    """Simulate affected components extraction"""
    if "LoginPage.js" in log:
        return "src/components/LoginPage.js"
    elif "UserService.java" in log:
        return "src/services/UserService.java"
    elif "Jenkinsfile" in log:
        return "Jenkinsfile"
    else:
        return "unknown-file.js"

def get_severity_assessment(log):
    """Simulate severity assessment"""
    if "500" in log or "Exception" in log:
        return "High"
    elif "AssertionError" in log:
        return "Medium"
    else:
        return "Low"

if __name__ == "__main__":
    test_bug_assignment_analysis() 