import pip
while True:
    try:
        from selenium import webdriver
        from selenium.webdriver.common.by import By
        from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        from datetime import datetime
        from datetime import time as dttime
        import time, json, os, sys, re
        break
    except:
        if (input("Do you wanna install these requests [Y/n]").lower() == ("y" or "")):
            pip.main(['install', "-r", "requirements.txt"])
        else:
            print("Program won't run without requirements")
            exit()


print(len(sys.argv))
print(sys.argv)

configJson = "configTest.json"

valURL = re.compile( # regex to see if valid url
    r'^(?:http|ftp)s?://' # http:// or https://
    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
    r'localhost|' #localhost...
    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
    r'(?::\d+)?' # optional port
    r'(?:/?|[/?]\S+)$', re.IGNORECASE)


class getPDF:
    def __init__(self, url, webDriverPath="./chromedriver", browser=None, browserHide = False):
        #url of the page we want to run
        self.url = url
        self.webDriverPath = webDriverPath
        self.browser = browser
        self.browserHide = browserHide

    def waitUrlChange(self, currentURL): # function to wait for next page to load before continuing 
        WebDriverWait(self.driver, 10).until(lambda driver: driver.current_url != currentURL)

    def autoLogin(self):
        while True:
            currentUrl = self.driver.current_url
            if currentUrl.find("https://www.mynelson.com/mynelson/staticcontent/html/PublicLogin.html") != -1: # logs you in to google in order to access the link provided 
                print("Logging in to mynelson...")
                with open(configJson, "r") as read_file: # puts email in to google login from configJson
                    data = json.load(read_file)
                    login = self.driver.find_element_by_css_selector(".whsOnd.zHQkBf")
                    login.send_keys(data["user"]["email"])
                    self.driver.find_element_by_class_name("VfPpkd-dgl2Hf-ppHlrf-sM5MNb").click()
                self.waitUrlChange(currentUrl)
            else:
                break
        pass

    def fillForm(self):
        while True:
            currentUrl = self.driver.current_url
            if currentUrl.find("https://docs.google.com/forms/d/e/1FAIpQLSedNWLgRdQKVfNqT4gwYrq0PEJqj2vnOL5GHqfopjwnakC-0g/viewform") != -1: # fills out form 
                print("Filling out form...")
                with open(configJson, "r") as read_file: # puts email in to google login from configJson
                    data = json.load(read_file)
                    textBoxes = self.driver.find_elements_by_class_name("quantumWizTextinputPaperinputInput")
                    textBoxes[0].send_keys(data["user"]["firstName"])
                    textBoxes[1].send_keys(data["user"]["lastName"])
                    radioButton = self.driver.find_elements_by_class_name("appsMaterialWizToggleRadiogroupOffRadio")
                    radioButton[0].click()
                    time.sleep(5)
                    submit = self.driver.find_element_by_class_name("appsMaterialWizButtonPaperbuttonContent")
                    submit.click()
                self.waitUrlChange(currentUrl)
                break
            elif currentUrl.find("https://docs.google.com/forms/d/e/1FAIpQLSedNWLgRdQKVfNqT4gwYrq0PEJqj2vnOL5GHqfopjwnakC-0g/closedform") != -1: 
                print("Form is closed")
                break
            elif currentUrl.find("https://docs.google.com/forms/d/e/1FAIpQLSedNWLgRdQKVfNqT4gwYrq0PEJqj2vnOL5GHqfopjwnakC-0g/alreadyresponded") != -1:
                print("Form already answered")
                break
            elif currentUrl.find("https://docs.google.com/forms/d/e/1FAIpQLSedNWLgRdQKVfNqT4gwYrq0PEJqj2vnOL5GHqfopjwnakC-0g/closedform") != -1:
                print("Form is closed")
                break


    def run(self):
        try:
            # set up
            caps = DesiredCapabilities().CHROME
            # caps["pageLoadStrategy"] = "normal"  #  complete
            #caps["pageLoadStrategy"] = "eager"  #  interactive
            # caps["pageLoadStrategy"] = "none"   #  undefined

            chromeOptions = webdriver.chrome.options.Options()
            if self.browserHide == True: # hides web browser if true
                chromeOptions.headless = True
            try:
                if self.browser != None: # uses chrome by default if put in another browser location trys to use that browser
                    chromeOptions.binary_location = self.browser
            except:
                print("Browser in that location does not exist")

            # initiating the webdriver. Parameter includes the path of the webdriver.
            self.driver = webdriver.Chrome(desired_capabilities=caps, executable_path=self.webDriverPath, options=chromeOptions)
            self.driver.get(self.url) # goes to starting url
            self.autoLogin()
            # self.fillForm()
        except Exception as err:
            print("Driver has stopped working\nShutting down...\n", err) # if something fails in the process of logging in to class it shuts down

    def quit(self):
        self.driver.quit() # quits webdriver



# Program starts running
if __name__ == '__main__':
    browserPath = ""
    with open(configJson, "r") as read_file:
        data = json.load(read_file)
        if os.path.isfile(data["browserPath"]):
            browserPath = data["browserPath"]

    #login
    # form = getPDF(url = "https://www.mynelson.com/mynelson/staticcontent/html/PublicLogin.html", browserHide = False, browser = browserPath)
    # form.run()
    # form.quit()
    pass