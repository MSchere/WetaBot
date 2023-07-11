from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.safari.options import Options as SafariOptions


class Utils:
    def setupDriver(self, browser, headless):
        chrome_options = ChromeOptions()
        firefox_options = FirefoxOptions()
        edge_options = EdgeOptions()
        safari_options = SafariOptions()
        
        if headless:
            if browser == 'opera' or browser == 'phantomjs':
                print('Browser not supported in headless mode')
                exit(1)
            chrome_options.add_argument('--headless')
            firefox_options.add_argument('--headless')
            edge_options.add_argument('--headless')
            safari_options.add_argument('--headless')

        if browser == 'chrome':
            drv = webdriver.Chrome(options=chrome_options)
        elif browser == 'firefox':
            drv = webdriver.Firefox(options=firefox_options)
        elif browser == 'edge':
            drv = webdriver.Edge(options=edge_options)
        elif browser == 'safari':
            drv = webdriver.Safari(options=safari_options)
        elif browser == 'opera':
            drv = webdriver.Opera()
        elif browser == 'phantomjs':
            drv = webdriver.PhantomJS()
        else:
            print('Browser not supported')
            exit(1)
        self.drv = drv
        return drv
    
    def setupActionChains(self, drv):
        self.act = ActionChains(drv)
        return ActionChains(drv)
        
    def click(self, xpath):
        # print("Clicking " + xpath)
        while True:
            try:
                self.drv.find_element(By.XPATH, xpath).click()
            except:
                continue
            break

    def inputText(self, text, xpath):
        # print("Inputting text " + text + " in " + xpath)
        while True:
            try:
                self.drv.find_element(By.XPATH, xpath).send_keys(text)
            except:
                continue
            break

    def inputTextByCSS(self, text, css):
        # print("Inputting text " + text + " in " + css)
        while True:
            try:
                self.drv.find_element(By.CSS_SELECTOR, css).send_keys(text)
            except:
                continue
            break

    def getText(self, xpath):
        # print("Getting text from " + xpath)
        while True:
            try:
                return self.drv.find_element(By.XPATH, xpath).text
            except:
                continue
            
    def openLinkInNewTab(self, xpath):
        # print("Opening link in new tab " + xpath)
        while True:
            try:
                link = (self.drv.find_element(By.XPATH, xpath).get_attribute('href'))
            except:
                continue
            break
        self.drv.execute_script("window.open('');")
        self.drv.switch_to.window(self.drv.window_handles[1])
        self.drv.get(link)
            
    def sendKeys(self, keys):
        self.act.send_keys(keys).perform()
