import pip, time, json, os, sys, re
from datetime import datetime
from datetime import time as dttime
while True:
    try:
        from selenium import webdriver
        from selenium.webdriver.common.by import By
        from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        break
    except:
        print("Dependencies required for",os.path.basename(__file__)+":")
        with open(os.path.join(sys.path[0], "requirements.txt"), "r") as reqFile:
            req = reqFile.readline()
            print(req)
            answer = input("Do you wanna install these dependencies if not installed already [Y/n] ").lower()
        if (answer == "y" or answer == ""):
            pip.main(['install', "-r", os.path.join(sys.path[0], "requirements.txt")])
        else:
            print(os.path.basename(__file__),"won't run without the dependencies")
            exit()

configJson = "configTest.json"

def autoInstallChromeDriver(browserPath = None):
    if sys.platform == "win32": # checks to see if platform is windows
        if sys.getwindowsversion().major == 10: # checks to see if running windows 10
            possiblePaths = [os.environ["ProgramFiles"]+"\Google\Chrome\Application\chrome.exe",os.environ["ProgramFiles(x86)"]+"\Google\Chrome\Application\chrome.exe",os.environ["LocalAppData"]+"\Google\Chrome\Application\chrome.exe"]
            if browserPath == None: # if browser path is not predetermined runs through expected locations
                for path in possiblePaths:
                    if os.path.isfile(path):
                        browserPath = path
                        break
                    elif path == possiblePaths[-1]:
                        print("Chrome browser not found please download or set explicit location")
                        exit()
            else:
                if os.path.isfile(browserPath) == False: 
                    print(browserPath,"is not a valid path to file")
                    exit()
            print("Win 10", browserPath)
            print(os.popen("wmic datafile where 'name=\""+browserPath.replace("\\", "\\\\").replace("/", "\\\\")+"\"' get version").read().splitlines()[2])
            # wmic datafile where 'name="C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe"' get version
        else:
            print("Automatic drivers unable to be downloaded for Windows "+str(sys.getwindowsversion().major)+" go to \"https://chromedriver.chromium.org/downloads\" to download manually for your chrome based browser and put in the folder \""+os.path.dirname(__file__)+"\"")
    else:
        print("Automatic drivers unable to be downloaded for "+sys.platform+" go to \"https://chromedriver.chromium.org/downloads\" to download manually for your chrome based browser and put in the folder \""+os.path.dirname(__file__)+"\"")
    

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
                with open(os.path.join(sys.path[0], configJson), "r") as read_file: # puts email in to google login from configJson
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
    with open(os.path.join(sys.path[0], configJson), "r") as read_file:
        data = json.load(read_file)
        if os.path.isfile(data["browserPath"]):
            browserPath = data["browserPath"]
    autoInstallChromeDriver(browserPath = browserPath)
    #login
    # form = getPDF(url = "https://www.mynelson.com/mynelson/staticcontent/html/PublicLogin.html", browserHide = False, browser = browserPath)
    # form.run()
    # form.quit()
    pass