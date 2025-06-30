```javascript
const { Builder, By, Key, until } = require('selenium-webdriver');
const assert = require('assert');

let driver = new Builder().forBrowser('firefox').build();

driver.manage().setTimeouts( { implicit: 5000 } );

driver.get('http://yourwebsite.com/login');

driver.findElement(By.name('username')).sendKeys('validUsername');
driver.findElement(By.name('password')).sendKeys('validPassword', Key.RETURN);

driver.wait(until.titleIs('Dashboard'), 5000)
    .then(() => console.log('Successfully logged in and navigated to Dashboard'))
    .catch(async error => {
        console.error('Failed to navigate to Dashboard', error);
        let screenshot = await driver.takeScreenshot();
        require('fs').writeFileSync('error.png', screenshot, 'base64');
    });

driver.findElement(By.id('dashboard'))
    .then(element => assert.ok(element, 'Dashboard not found'))
    .catch(async error => {
        console.error('Dashboard not found', error);
        let screenshot = await driver.takeScreenshot();
        require('fs').writeFileSync('error.png', screenshot, 'base64');
    });

driver.quit();
```
Please replace 'http://yourwebsite.com/login', 'validUsername', 'validPassword', and 'Dashboard' with your actual values. Also, make sure that the dashboard has an id of 'dashboard'.