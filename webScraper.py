import selenium
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class webScraper:
    def __init__(self, url, webDriverPath="./chromedriver", browser=None, browserDownloadPath = None, browserHide = False, logLevel: int = None):
        #Sets up the variables for the webscraper class
        self.url = url
        self.webDriverPath = webDriverPath
        self.browser = browser
        self.browserDownloadPath = browserDownloadPath
        self.browserHide = browserHide
        self.logLevel = logLevel

    def waitUrlChange(self, currentURL: str, waitTime: int = 10): # function to wait for next page to load before continuing 
        try:
            WebDriverWait(self.driver, waitTime).until(lambda driver: driver.current_url != currentURL)
            return True
        except selenium.common.exceptions.TimeoutException:
            return False

    def setup(self):
        try:
            # set up
            caps = DesiredCapabilities().CHROME
            # caps["pageLoadStrategy"] = "normal"  #  complete
            # caps["pageLoadStrategy"] = "eager"  #  interactive
            # caps["pageLoadStrategy"] = "none"   #  undefined

            chromeOptions = webdriver.chrome.options.Options()
            if self.browserHide == True: # hides web browser if true
                chromeOptions.headless = True
            try:
                if self.browser != None: # uses chrome by default if put in another browser location trys to use that browser
                    chromeOptions.binary_location = self.browser
            except:
                print("Browser in that location does not exist")
            if self.browserDownloadPath != None:
                chromeOptions.add_experimental_option("prefs", {
                    "download.default_directory": self.browserDownloadPath,
                    "download.prompt_for_download": False # ,
                    # "download.directory_upgrade": True,
                    # "safebrowsing.enabled": True
                    })
            if self.logLevel != None:
                chromeOptions.add_argument("--log-level="+str(self.logLevel))
            # initiating the webdriver. Parameter includes the path of the webdriver.
            self.driver = webdriver.Chrome(desired_capabilities=caps, service=Service(self.webDriverPath), options=chromeOptions)
            self.driver.get(self.url) # goes to starting url
        except Exception as err:
            print("Driver initiation has stopped working\nShutting down...\n", err) # if something fails in the initiation process it shuts down

    def quit(self):
        self.driver.quit() # quits webdriver