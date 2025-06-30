```python
import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

class LoginTest(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get("http://www.yourwebsite.com/login")

    def test_login(self):
        driver = self.driver
        try:
            username = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "username")))
            password = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "password")))
            submit = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "submit")))
            
            username.send_keys("valid_username")
            password.send_keys("valid_password")
            submit.click()

            # Check if login was successful
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "user_welcome_message")))
        except NoSuchElementException as ex:
            self.take_screenshot()
            print(ex)
            self.fail("Element not found, see screenshot for details")

    def take_screenshot(self):
        self.driver.save_screenshot('screenshot.png')

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()
```
Please replace "http://www.yourwebsite.com/login", "username", "password", "submit", "valid_username", "valid_password", and "user_welcome_message" with your actual website URL, form field names, valid credentials, and welcome message element ID respectively.