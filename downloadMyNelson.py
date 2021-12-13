import time, json, os, sys, re, shutil, requests, selenium, autoChromeDriver
from bs4 import BeautifulSoup, SoupStrainer
from selenium.webdriver.common import by
from datetime import datetime
from datetime import time as dttime

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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
    def __init__(self, url, webDriverPath="./chromedriver", browser=None, browserDownloadPath = None, browserHide = False):
        #url of the page we want to run
        self.url = url
        self.webDriverPath = webDriverPath
        self.browser = browser
        self.browserDownloadPath = browserDownloadPath
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
            WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.ID, "txt-clear")))
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
            if self.browserDownloadPath != None:
                chromeOptions.add_experimental_option("prefs", {
                    "download.default_directory": self.browserDownloadPath,
                    "download.prompt_for_download": False # ,
                    # "download.directory_upgrade": True,
                    # "safebrowsing.enabled": True
                    })

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
        try:
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "productMain")))
            textbooks = [str(textbook.text).removeprefix("Loading...\n").replace("\n", " - ") for textbook in self.driver.find_elements(By.CLASS_NAME, "productMain")]
            self.quit()
            return textbooks
        except:
            self.quit()
    
    def makeTextbookDirectorys(self, name: str, textbooksNames: list = ["all"]):
        self.setup()
        self.autoLogin(name=name)
        try:
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
        except:
            self.quit()

    def downloadTextbook(self, name: str, textbookName: str):
        self.setup()
        self.autoLogin(name=name)
        # try:
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "productMain")))
        textbooks = self.driver.find_elements(By.CLASS_NAME, "productMain")
        for textbook in textbooks:
            if str(textbook.text).removeprefix("Loading...\n").replace("\n", " - ") == textbookName:
                pagesPath = os.path.join(sys.path[0],"users",name,str(textbook.text).removeprefix("Loading...\n").replace("\n", " - "),datetime.now().strftime("%d/%m/%Y-%H:%M:%S"),"tmp")
                os.makedirs(pagesPath)
                self.driver.get(textbook.find_element(By.CSS_SELECTOR, "a[title=\""+textbookName+"\"]").get_attribute('href'))

                """
                Okay lots of recursion 
                Find by class="ul accordion" in this contain all the levels of the textbook
                Once found get all class="li depth"+n 

                """
                # on textbook page
                
                WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, "jspPane")))
                #contentLocation = self.driver.find_element(By.CLASS_NAME, "jspPane").find_element(By.XPATH, "./*")
                contentLocation = self.driver.find_elements(By.CLASS_NAME, "jspPane")[[i.find_element(By.XPATH, "./*").get_attribute('class') for i in self.driver.find_elements(By.CLASS_NAME, "jspPane")].index("ul accordion")].find_element(By.XPATH, "./*")  
                def clickLevel(currentLevel, level: int):
                    current = "depth"+str(level)
                    print(current)
                    sections = currentLevel.find_elements(By.XPATH, "./*")
                    for i in sections:
                        actions = ActionChains(self.driver)
                        actions.move_to_element(i).perform()
                        if "content" == i.get_attribute('class'):
                            i.click()
                            print("Found content")
                            WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, "linkRowContainer")))
                            links = self.driver.find_elements(By.CLASS_NAME, "linkRowContainer")
                            for link in links:
                                if "PDF" in link.find_element(By.XPATH, "./*").get_attribute('class'):
                                    PDFDownload = link.find_element(By.CLASS_NAME, "link_NotDownloadable").get_attribute('openlink')
                                    print(PDFDownload)
                                    self.driver.execute_script("window.open('about:blank', 'secondtab');")
                                    self.driver.switch_to.window(window_name=self.driver.window_handles[1])
                                    self.driver.get(PDFDownload)
                                    def every_downloads_chrome(driver):
                                        if not driver.current_url.startswith("chrome://downloads"):
                                            driver.get("chrome://downloads/")
                                        return driver.execute_script("""
                                            var items = document.querySelector('downloads-manager')
                                                .shadowRoot.getElementById('downloadsList').items;
                                            if (items.every(e => e.state === "COMPLETE"))
                                                return items.map(e => e.fileUrl || e.file_url);
                                            """)
                                    downloadPaths = WebDriverWait(self.driver, 120, 1).until(every_downloads_chrome)
                                    WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.CLASS_NAME, "icon-clear")))
                                    print(self.driver.find_elements(By.CLASS_NAME, "icon-clear"))
                                    for clickx in self.driver.find_elements(By.CLASS_NAME, "icon-clear"):
                                        clickx.click()
                                    time.sleep(3)
                                    self.driver.close()
                                    self.driver.switch_to.window(window_name=self.driver.window_handles[0])
                                    for chromeDownloadPath in downloadPaths:
                                        try:
                                            downloadPath = str(chromeDownloadPath).removeprefix("file://").replace("%20"," ")
                                            shutil.move(downloadPath, os.path.join(pagesPath,str((sorted([int(os.path.splitext(file)[0]) for file in os.listdir(pagesPath)], reverse=True)[0]+1 if os.listdir(pagesPath) else 1))+os.path.splitext(os.path.basename(downloadPath))[-1]))
                                        except:
                                            pass

                            # print(self.driver.find_element(By.ID, "col2").find_element(By.ID, "linkList_Container").find_element(By.XPATH, "./*").get_attribute('class'))
                            # for j in self.driver.find_element(By.ID, "col2").find_elements(By.ID, "linkList_Container"): #.find_elements(By.XPATH, "./*")
                            #     print(j.get_attribute('class'))
                            # time.sleep(4)
                            
                            # print(self.driver.find_element(By.XPATH, "/html/body/div[2]/div/div/div[2]/div[4]/div/div[1]/div/div/div/div[1]/div/div[1]"))

                            # html_page = self.driver.page_source # gets webpage data
                            # soup = BeautifulSoup(html_page, features="lxml", parse_only=SoupStrainer('a')) # into bs object

                            # links = []
                            # for link in soup.findAll('a'): # goes throught all the links in the html file and gets the ones with the keyword
                            #     print(link.get('openlink'))
                            #     if "PDF" in str(link.get('href')):
                            #         links.append(link.get('href'))
                            # return links[0] # returns first instance as it is probably 99% of the time the correct link










                            # print(self.driver.find_elements(By.CLASS_NAME, "jspPane"))
                            # elems  = self.driver.find_element(By.ID, "col2").find_elements(By.CLASS_NAME, "link_NotDownloadable") # .find_element(By.XPATH, "./*").get_attribute('class')          .find_element(By.ID, "linkList_Container").find_element(By.XPATH, "./*")
                            # print(elems)
                            # for elem in elems:
                            #     print(elem.get_attribute("openlink"))
                            #     if "PDF" in elem.get_attribute("openlink"):
                            #         print(elem.get_attribute("openlink"))
                            # print(self.driver.find_element(By.ID, "col2").find_element(By.ID, "linkList_Container").find_element(By.XPATH, "./*").find_element(By.XPATH, "./*"))
                            # print("hello")
                            # print([i.find_element(By.XPATH, "./*").get_attribute('class') for i in self.driver.find_elements(By.CLASS_NAME, "jspPane")])
                            # for content in self.driver.find_elements(By.CLASS_NAME, "jspPane")[[i.find_element(By.XPATH, "./*").get_attribute('id') for i in self.driver.find_elements(By.CLASS_NAME, "jspPane")].index("linkList")].find_element(By.XPATH, "./*"):
                            #     print(content)
                            #     print(content.find_element(By.XPATH, "./*").get_attribute('class'))
                            # self.driver.execute_script("window.open('about:blank', 'secondtab');")
                            # self.driver.switch_to.window(window_name=self.driver.window_handles[1])
                            # print("here2")
                            # self.driver.get("https://www.google.ca/")
                            # self.driver.close()
                            # self.driver.switch_to.window(window_name=self.driver.window_handles[0])
                            # print(self.driver.window_handles)
                            # time.sleep(5)
                            # self.quit()
                        elif current in i.get_attribute('class'):
                            print([j.get_attribute('class') for j in i.find_elements(By.XPATH, "./*")])
                            i.click()
                            print([j.get_attribute('class') for j in i.find_elements(By.XPATH, "./*")])
                            clickLevel(currentLevel = i.find_elements(By.XPATH, "./*")[[j.get_attribute('class') for j in i.find_elements(By.XPATH, "./*")].index("ul" if "ul" in [j.get_attribute('class') for j in i.find_elements(By.XPATH, "./*")] else "ul backgroundNone")], level = level+1)
                clickLevel(currentLevel=contentLocation, level=1)
                print("Here")
        self.quit()
        # except:
        #     self.quit()
# Program starts running
if __name__ == '__main__':
    browserPath = ""
    with open(os.path.join(sys.path[0], configJson), "r") as read_file:
        data = json.load(read_file)
        if os.path.isfile(data["browserPath"]):
            browserPath = data["browserPath"]
    # config.gen()
    # config.userDelete(name="a")
    # autoChromeDriver.autoInstall(browserPath = browserPath)
    #login
    form = myNelson(url = "https://www.mynelson.com/mynelson/staticcontent/html/PublicLogin.html", browserHide = False, browser = browserPath, browserDownloadPath=os.path.join(sys.path[0], "tmp"))
    # form.run()
    # print(form.testLogin("user1"))
    # print(form.getTextbookList(name="user1"))
    # form.makeTextbookDirectorys(name="user1", textbooksNames=["Chemistry 12U - Student Text PDF (Online)"])
    form.downloadTextbook(name="user1", textbookName="Chemistry 12U - Student Text PDF (Online)")
    # form.downloadTextbooks()
    # form.quit()
    pass