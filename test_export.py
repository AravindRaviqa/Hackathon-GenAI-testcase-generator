#!/usr/bin/env python3
"""
Test script to verify export functionality for user stories
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import JiraTestCaseGenerator, generate_test_cases, parse_test_cases

def test_user_story_export():
    """Test the export functionality for user stories"""
    print("Testing user story export functionality...")
    
    # Sample user story
    user_story = """
    As a user, I want to be able to log in to the system
    So that I can access my account and perform actions
    """
    
    # Generate test cases
    print("1. Generating test cases...")
    tc = generate_test_cases(user_story)
    parsed = parse_test_cases(tc)
    
    structured_test_cases = [{
        'user_story': user_story,
        'test_cases': parsed
    }]
    
    print(f"   Generated {len(parsed)} test cases")
    
    # Test PDF generation
    print("2. Testing PDF generation...")
    generator = JiraTestCaseGenerator()
    try:
        pdf_data = generator.generate_pdf_for_user_stories(structured_test_cases, "Test User Story")
        print(f"   PDF generated successfully ({len(pdf_data)} bytes)")
        
        # Save test PDF
        pdf_path = "static/temp/test_user_story_export.pdf"
        os.makedirs(os.path.dirname(pdf_path), exist_ok=True)
        with open(pdf_path, 'wb') as f:
            f.write(pdf_data)
        print(f"   PDF saved to {pdf_path}")
        
    except Exception as e:
        print(f"   Error generating PDF: {e}")
        return False
    
    # Test Excel generation
    print("3. Testing Excel generation...")
    try:
        import pandas as pd
        
        export_test_cases = []
        for case in structured_test_cases:
            for test_case in case['test_cases']:
                export_test_cases.append({
                    'User Story': case['user_story'][:100] + '...' if len(case['user_story']) > 100 else case['user_story'],
                    'Test Case': test_case
                })
        
        if export_test_cases:
            test_cases_df = pd.DataFrame(export_test_cases)
            excel_path = "static/temp/test_user_story_export.xlsx"
            test_cases_df.to_excel(excel_path, index=False)
            print(f"   Excel file saved to {excel_path}")
        else:
            print("   No test cases to export")
            
    except Exception as e:
        print(f"   Error generating Excel: {e}")
        return False
    
    print("✅ All export tests passed!")
    return True

if __name__ == "__main__":
    success = test_user_story_export()
    sys.exit(0 if success else 1) 