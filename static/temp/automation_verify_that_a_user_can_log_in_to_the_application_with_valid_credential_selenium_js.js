```javascript
const { Builder, By, Key, until } = require('selenium-webdriver');
const assert = require('assert');

let driver = new Builder().forBrowser('firefox').build();

driver.manage().window().maximize();

driver.get('http://your-application-url.com/login');

driver.findElement(By.name('username')).sendKeys('validUsername');
driver.findElement(By.name('password')).sendKeys('validPassword', Key.RETURN);

driver.wait(until.urlContains('dashboard'), 10000)
    .then(function(result) {
        assert.strictEqual(result, true, 'User was not able to login');
    })
    .catch(function(error) {
        driver.takeScreenshot().then(function(screenShot) {
            require('fs').writeFileSync('error.png', screenShot, 'base64');
        });
        console.error('An error occurred: ', error);
    })
    .finally(function() {
        driver.quit();
    });
```