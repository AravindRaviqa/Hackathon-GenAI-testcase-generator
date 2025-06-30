```python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import unittest
import time

class TestLogin(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get("http://www.example.com/login")  # replace with your website URL

    def test_login(self):
        try:
            username = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "username"))  # replace with your username field ID
            )
            password = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "password"))  # replace with your password field ID
            )
            submit = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "submit"))  # replace with your submit button ID
            )

            username.send_keys("testuser")  # replace with your username
            password.send_keys("testpassword")  # replace with your password
            submit.click()

            dashboard = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "dashboard"))  # replace with your dashboard element ID
            )

            self.assertTrue(dashboard.is_displayed())
        except TimeoutException as ex:
            self.driver.save_screenshot('screenshot.png')
            print("Exception has been thrown. " + str(ex))
            self.fail("Test failed due to timeout")
        except NoSuchElementException as ex:
            self.driver.save_screenshot('screenshot.png')
            print("Exception has been thrown. " + str(ex))
            self.fail("Test failed due to element not found")

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()
```