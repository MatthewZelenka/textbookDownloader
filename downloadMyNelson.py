import time, json, os, sys, shutil, requests, webScraper
from datetime import datetime
from datetime import time as dttime

import selenium, autoChromeDriver
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

configJson = "config.json"

class config():
    @staticmethod
    def gen():
        baseConfig = {
            "browserPath":"",
            "users":{}
        }
        with open(os.path.join(sys.path[0],configJson), "w") as confFile:
            confFile.write(json.dumps(baseConfig, indent=4))
        os.makedirs(os.path.join(sys.path[0],"users"))
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
        os.makedirs(os.path.join(sys.path[0],"users",(username if name == None else name)))
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
    @staticmethod
    def userEdit(name: str, newEmail: str = None, newPassword: str = None, newName: str = None):
        data: dict
        with open(os.path.join(sys.path[0], configJson), "r") as confFile: # 
            data = json.load(confFile)
        if newEmail:
            data["users"][name]["email"] = newEmail
        if newPassword:
            data["users"][name]["password"] = newEmail
        if newName:
            data["users"][newName] = data["users"].pop(name)
        with open(os.path.join(sys.path[0],configJson), "w") as confFile:
            confFile.write(json.dumps(data, indent=4))      

class myNelson(webScraper.webScraper):
    def autoLogin(self, name, waitUrlChange:bool = True, waitTime: int = 10):
        currentUrl = self.driver.current_url
        try:
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
        except:
            self.quit()

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
                        os.makedirs(os.path.join(sys.path[0],"users",name,str(textbook.text).removeprefix("Loading...\n").replace("\n", " - ")))
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
        try:
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "productMain")))
            textbooks = self.driver.find_elements(By.CLASS_NAME, "productMain")
            textbook = textbooks[[str(textbook.text).removeprefix("Loading...\n").replace("\n", " - ") for textbook in textbooks].index(textbookName)]
            pagesPath = os.path.join(sys.path[0],"users",name,str(textbook.text).removeprefix("Loading...\n").replace("\n", " - "),datetime.now().strftime("%d-%m-%Y_%Hh-%Mm-%Ss"),"tmp")
            print(pagesPath)
            os.makedirs(pagesPath)
            self.driver.get(textbook.find_element(By.CSS_SELECTOR, "a[title=\""+textbookName+"\"]").get_attribute('href'))
            WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, "jspPane")))
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
                                self.driver.close()
                                self.driver.switch_to.window(window_name=self.driver.window_handles[0])
                                if sys.platform == "win32":
                                    downloadPath = str(downloadPaths[0]).removeprefix("file:///").replace("%20"," ")
                                elif sys.platform == "linux":
                                    downloadPath = str(downloadPaths[0]).removeprefix("file://").replace("%20"," ")
                                shutil.move(downloadPath, os.path.join(pagesPath,str((sorted([int(os.path.splitext(file)[0]) for file in os.listdir(pagesPath)], reverse=True)[0]+1 if os.listdir(pagesPath) else 1))+os.path.splitext(os.path.basename(downloadPath))[-1]))
                    elif current in i.get_attribute('class'):
                        print([j.get_attribute('class') for j in i.find_elements(By.XPATH, "./*")])
                        i.click()
                        print([j.get_attribute('class') for j in i.find_elements(By.XPATH, "./*")])
                        clickLevel(currentLevel = i.find_elements(By.XPATH, "./*")[[j.get_attribute('class') for j in i.find_elements(By.XPATH, "./*")].index("ul" if "ul" in [j.get_attribute('class') for j in i.find_elements(By.XPATH, "./*")] else "ul backgroundNone")], level = level+1)
            clickLevel(currentLevel=contentLocation, level=1)
            self.quit()
        except Exception as err:
            print(err)
            self.quit()
    
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
    form = myNelson(url = "https://www.mynelson.com/mynelson/staticcontent/html/PublicLogin.html", browserHide = False, browser = browserPath, browserDownloadPath=os.path.join(sys.path[0], "tmp"), logLevel = 3)
    print(form.testLogin("user1"))
    # print(form.getTextbookList(name="user1"))
    # form.makeTextbookDirectorys(name="user1", textbooksNames=["all"])
    # form.downloadTextbook(name="user1", textbookName="Chemistry 12U - Student Text PDF (Online)")
    # form.downloadTextbook(name="user1", textbookName="Physics 11U - Online Student Text PDF Files")
    pass