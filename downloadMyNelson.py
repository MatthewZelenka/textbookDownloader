import pip, time, json, os, sys, re, shutil, requests
from datetime import datetime
from datetime import time as dttime

import selenium
while True:
    try:
        import autoChromeDriver
        from selenium import webdriver
        from selenium.webdriver.common.by import By
        from selenium.webdriver.chrome.service import Service
        from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        break
    except:
        if __name__ == '__main__':
            print("Dependencies required for",os.path.basename(__file__)+":")
            with open(os.path.join(sys.path[0], "requirements.txt"), "r") as reqFile:
                req = reqFile.read()
                print(req)
                answer = input("Do you wanna install these dependencies if not installed already [Y/n] ").lower()
            if (answer == "y" or answer == ""):
                pip.main(['install', "-r", os.path.join(sys.path[0], "requirements.txt")])
            else:
                print(os.path.basename(__file__),"won't run without the dependencies")
                exit()
        else:
            raise

configJson = "config.json"    

valURL = re.compile( # regex to see if valid url
    r'^(?:http|ftp)s?://' # http:// or https://
    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
    r'localhost|' #localhost...
    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
    r'(?::\d+)?' # optional port
    r'(?:/?|[/?]\S+)$', re.IGNORECASE)

class config():
    @staticmethod
    def gen():
        baseConfig = {
            "browserPath":"",
            "users":{}
        }
        with open(os.path.join(sys.path[0],configJson), "w") as confFile:
            confFile.write(json.dumps(baseConfig, indent=4))
        os.mkdir(os.path.join(sys.path[0],"users"))
    @staticmethod
    def listUsers():
        with open(os.path.join(sys.path[0], configJson), "r") as confFile: # 
            return list(json.load(confFile)["Users"].keys())
    @staticmethod
    def userAdd(username: str, password: str, name: str = None):
        data: dict
        with open(os.path.join(sys.path[0], configJson), "r") as confFile: # 
            data = json.load(confFile)
        data["users"].update({(username if name == None else name):{"email": username, "password": password}})
        with open(os.path.join(sys.path[0],configJson), "w") as confFile:
            confFile.write(json.dumps(data, indent=4))
        os.mkdir(os.path.join(sys.path[0],"users",(username if name == None else name)))
    @staticmethod
    def userDelete(name: str):
        try:
            shutil.rmtree(os.path.join(sys.path[0],"users",name))
            data: dict
            with open(os.path.join(sys.path[0], configJson), "r") as confFile: # 
                data = json.load(confFile)
            data["users"].pop(name)
            with open(os.path.join(sys.path[0],configJson), "w") as confFile:
                confFile.write(json.dumps(data, indent=4))
        except OSError as e:
            print("Error: %s - %s." % (e.filename, e.strerror))

class myNelson:
    def __init__(self, url, webDriverPath="./chromedriver", browser=None, browserHide = False):
        #url of the page we want to run
        self.url = url
        self.webDriverPath = webDriverPath
        self.browser = browser
        self.browserHide = browserHide

    def waitUrlChange(self, currentURL: str, waitTime: int = 10): # function to wait for next page to load before continuing 
        try:
            WebDriverWait(self.driver, waitTime).until(lambda driver: driver.current_url != currentURL)
            return True
        except selenium.common.exceptions.TimeoutException:
            return False


    def autoLogin(self, name, waitUrlChange:bool = True, waitTime: int = 10):
        currentUrl = self.driver.current_url
        if currentUrl.find("https://www.mynelson.com/mynelson/staticcontent/html/PublicLogin.html") != -1: # logs you in to google in order to access the link provided 
            print("Logging in to mynelson...")
            with open(os.path.join(sys.path[0], configJson), "r") as read_file: # puts email in to google login from configJson
                data = json.load(read_file)
                # Clicks and inputs username
                self.driver.find_element(By.ID, "txt-clear").click()
                self.driver.find_element(By.ID, "txtUName").send_keys(data["users"][name]["email"])
                # Clicks and inputs password
                self.driver.find_element(By.ID, "password-clear").click()
                self.driver.find_element(By.ID, "txtPwd").send_keys(data["users"][name]["password"])
                # Clicks on login
                self.driver.find_element(By.ID, "btnLogin").click()
            if waitUrlChange == True: self.waitUrlChange(currentURL=currentUrl, waitTime=waitTime)
        pass

    def fillForm(self):
        while True:
            currentUrl = self.driver.current_url
            if currentUrl.find("https://docs.google.com/forms/d/e/1FAIpQLSedNWLgRdQKVfNqT4gwYrq0PEJqj2vnOL5GHqfopjwnakC-0g/viewform") != -1: # fills out form 
                print("Filling out form...")
                with open(os.path.join(sys.path[0], configJson), "r") as read_file: # puts email in to google login from configJson
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

            # initiating the webdriver. Parameter includes the path of the webdriver.
            self.driver = webdriver.Chrome(desired_capabilities=caps, service=Service(self.webDriverPath), options=chromeOptions)
            self.driver.get(self.url) # goes to starting url
            # self.autoLogin()
            # self.fillForm()
        except Exception as err:
            print("Driver has stopped working\nShutting down...\n", err) # if something fails in the process of logging in to class it shuts down

    def quit(self):
        self.driver.quit() # quits webdriver

    def testLogin(self, name):
        self.setup()
        currentUrl = self.driver.current_url
        self.autoLogin(name=name, waitUrlChange=True, waitTime=2)
        result = False if currentUrl == self.driver.current_url else True
        self.quit()
        return result
    
    def getTextbookList(self, name: str):
        self.setup()
        self.autoLogin(name=name)
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "productMain")))
        textbooks = [str(textbook.text).removeprefix("Loading...\n").replace("\n", " - ") for textbook in self.driver.find_elements(By.CLASS_NAME, "productMain")]
        self.quit()
        return textbooks
    
    def makeTextbookDirectorys(self, name: str, textbooksNames: list = ["all"]):
        self.setup()
        self.autoLogin(name=name)
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "productMain")))
        textbooks = self.driver.find_elements(By.CLASS_NAME, "productMain")
        for textbook in textbooks:
            if "all" in textbooksNames or str(textbook.text).removeprefix("Loading...\n").replace("\n", " - ") in textbooksNames:
                try:
                    os.mkdir(os.path.join(sys.path[0],"users",name,str(textbook.text).removeprefix("Loading...\n").replace("\n", " - ")))
                except FileExistsError:
                    pass
                r = requests.get(textbook.find_element(By.CLASS_NAME, "prodImage").get_attribute('src'), allow_redirects=True)
                with open(os.path.join(os.path.join(sys.path[0],"users",name,str(textbook.text).removeprefix("Loading...\n").replace("\n", " - "),"cover.png")), 'wb') as cover:
                    cover.write(r.content)
                    cover.close()
                
        self.quit()

# Program starts running
if __name__ == '__main__':
    browserPath = ""
    with open(os.path.join(sys.path[0], configJson), "r") as read_file:
        data = json.load(read_file)
        if os.path.isfile(data["browserPath"]):
            browserPath = data["browserPath"]
    # config.gen()
    config.userDelete(name="a")
    # autoChromeDriver.autoInstall(browserPath = browserPath)
    #login
    form = myNelson(url = "https://www.mynelson.com/mynelson/staticcontent/html/PublicLogin.html", browserHide = False, browser = browserPath)
    # form.run()
    # print(form.testLogin("user1"))
    print(form.getTextbookList(name="user1"))
    form.makeTextbookDirectorys(name="user1", textbooksNames=["Chemistry 12U - Student Text PDF (Online)"])
    # form.downloadTextbooks()
    # form.quit()
    pass