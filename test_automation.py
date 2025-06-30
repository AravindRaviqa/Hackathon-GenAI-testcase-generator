#!/usr/bin/env python3
"""
Test script to demonstrate the Natural Language to Automation Script feature
"""

import requests
import json

def test_automation_generation():
    """Test the automation script generation functionality"""
    
    # Test scenarios
    test_scenarios = [
        {
            "scenario": "Login with valid credentials and check dashboard",
            "framework": "selenium_python",
            "expected_features": ["WebDriver setup", "login form", "dashboard verification", "screenshot"]
        },
        {
            "scenario": "Navigate to product page, add item to cart, and verify checkout process",
            "framework": "playwright_js",
            "expected_features": ["browser setup", "navigation", "cart functionality", "checkout"]
        }
    ]
    
    print("🤖 Testing Natural Language to Automation Script Feature")
    print("=" * 60)
    
    for i, test in enumerate(test_scenarios, 1):
        print(f"\n📝 Test Case {i}: {test['scenario']}")
        print(f"🔧 Framework: {test['framework']}")
        print(f"✅ Expected Features: {', '.join(test['expected_features'])}")
        
        # Simulate the AI generation process
        print("🔄 Generating automation script...")
        
        # This would normally call the OpenAI API
        # For demo purposes, we'll show what the output would look like
        if test['framework'] == 'selenium_python':
            demo_script = generate_demo_selenium_python(test['scenario'])
        elif test['framework'] == 'playwright_js':
            demo_script = generate_demo_playwright_js(test['scenario'])
        else:
            demo_script = "# Demo script would be generated here"
        
        print("📄 Generated Script Preview:")
        print("-" * 40)
        print(demo_script[:200] + "..." if len(demo_script) > 200 else demo_script)
        print("-" * 40)
        
        # Simulate file generation
        filename = f"demo_automation_{i}_{test['framework']}.py"
        print(f"💾 Script saved as: {filename}")
        
    print("\n🎉 Automation script generation test completed!")
    print("\n🚀 To use this feature:")
    print("1. Start the Flask application: python app.py")
    print("2. Open your browser to http://localhost:5000")
    print("3. Scroll down to the 'Natural Language to Automation Script' section")
    print("4. Enter your test scenario and choose your framework")
    print("5. Click 'Generate Automation Script'")

def generate_demo_selenium_python(scenario):
    """Generate a demo Selenium Python script"""
    return f'''import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import os

class TestAutomation:
    def __init__(self):
        self.driver = None
        self.wait = None
    
    def setup_driver(self):
        """Setup Chrome WebDriver with options"""
        chrome_options = Options()
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        
        service = Service("chromedriver.exe")  # Update path as needed
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.wait = WebDriverWait(self.driver, 10)
    
    def take_screenshot(self, name="screenshot"):
        """Take screenshot on failure"""
        if not os.path.exists("screenshots"):
            os.makedirs("screenshots")
        self.driver.save_screenshot(f"screenshots/{{name}}_{{int(time.time())}}.png")
    
    def test_scenario(self):
        """Test scenario: {scenario}"""
        try:
            # Navigate to the application
            self.driver.get("https://example.com")
            
            # Your automation steps would be generated here based on the scenario
            print(f"Executing scenario: {scenario}")
            
            # Example login steps (would be customized based on scenario)
            username_field = self.wait.until(
                EC.presence_of_element_located((By.ID, "username"))
            )
            username_field.send_keys("testuser")
            
            password_field = self.driver.find_element(By.ID, "password")
            password_field.send_keys("testpass")
            
            login_button = self.driver.find_element(By.ID, "login-btn")
            login_button.click()
            
            # Verify successful login
            dashboard = self.wait.until(
                EC.presence_of_element_located((By.CLASS_NAME, "dashboard"))
            )
            assert dashboard.is_displayed(), "Dashboard not displayed after login"
            
            print("✅ Test scenario completed successfully!")
            
        except Exception as e:
            print(f"❌ Test failed: {{str(e)}}")
            self.take_screenshot("test_failure")
            raise
        finally:
            self.cleanup()
    
    def cleanup(self):
        """Clean up resources"""
        if self.driver:
            self.driver.quit()

if __name__ == "__main__":
    test = TestAutomation()
    test.setup_driver()
    test.test_scenario()
'''

def generate_demo_playwright_js(scenario):
    """Generate a demo Playwright JavaScript script"""
    return f'''const {{ chromium }} = require('playwright');

class TestAutomation {{
    constructor() {{
        this.browser = null;
        this.page = null;
    }}
    
    async setup() {{
        this.browser = await chromium.launch({{ headless: false }});
        this.page = await this.browser.newPage();
    }}
    
    async takeScreenshot(name = 'screenshot') {{
        const fs = require('fs');
        if (!fs.existsSync('./screenshots')) {{
            fs.mkdirSync('./screenshots');
        }}
        await this.page.screenshot({{ 
            path: `./screenshots/${{name}}_${{Date.now()}}.png` 
        }});
    }}
    
    async testScenario() {{
        try {{
            // Navigate to the application
            await this.page.goto('https://example.com');
            
            // Your automation steps would be generated here based on the scenario
            console.log(`Executing scenario: {scenario}`);
            
            // Example e-commerce steps (would be customized based on scenario)
            await this.page.click('#products-link');
            await this.page.waitForSelector('.product-item');
            
            await this.page.click('.product-item:first-child .add-to-cart');
            await this.page.waitForSelector('.cart-count');
            
            await this.page.click('#checkout-btn');
            await this.page.waitForSelector('#checkout-form');
            
            // Fill checkout form
            await this.page.fill('#email', 'test@example.com');
            await this.page.fill('#name', 'Test User');
            await this.page.fill('#address', '123 Test St');
            
            await this.page.click('#submit-order');
            await this.page.waitForSelector('.order-confirmation');
            
            const confirmation = await this.page.textContent('.order-confirmation');
            console.log('✅ Test scenario completed successfully!');
            console.log('Order confirmation:', confirmation);
            
        }} catch (error) {{
            console.error('❌ Test failed:', error.message);
            await this.takeScreenshot('test_failure');
            throw error;
        }} finally {{
            await this.cleanup();
        }}
    }}
    
    async cleanup() {{
        if (this.browser) {{
            await this.browser.close();
        }}
    }}
}}

async function runTest() {{
    const test = new TestAutomation();
    await test.setup();
    await test.testScenario();
}}

runTest().catch(console.error);
'''

if __name__ == "__main__":
    test_automation_generation() 