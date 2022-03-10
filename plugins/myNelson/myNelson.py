# general imports
import pathlib, os, requests

# relitive imports
from lib.webScraper import *

# login function imports
from lib import autoLogin
import myNelsonLoginProcedure


plugName = pathlib.Path(__file__).stem

"""
function to test login credentials (login and returns true)

function to get textbooks on the side (login and once in gets list of textbooks)
    function to get textbook cover if exists updates every time

function to download textbook off site

function to merge pdf

function to make profile
"""

class myNelson(baseChromeWebScraper):
    def __init__(self, profile, webDriverPath:str = os.path.join(os.path.dirname(__file__),"chromedriver"), autoWebDriverModule:str = "lib.autoChromeDriver", browser:str = None, browserDownloadPath:str = None, browserHide:str = False, userAgent:str = None, logLevel: int = None):
        self.profile = profile
        super().__init__(webDriverPath, autoWebDriverModule, browser, browserDownloadPath, browserHide, userAgent, logLevel)

    def run(self):
        module = self.modules[[importedModule.plugName for importedModule in self.modules].index(self.profile["id"])]
        self.url = module.form
        self.setup()
        module.fillForm(self, self.profile)
    
    def __login(self):
        self.driver.get("https://www.mynelson.com/mynelson/staticcontent/html/PublicLogin.html")
        try:
            autoLogin.login(self=self, profile=self.profile, pageProcedure=[myNelsonLoginProcedure.myNelsonLoginPage])
            return True
        except:
            return False
    
    def __getTextBookElements(self):
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "productMain")))
        elements = self.driver.find_elements(By.CLASS_NAME, "productMain")
        return elements
    
    def __getCookies(self):
        cookies = {}
        selenium_cookies = self.driver.get_cookies()
        for cookie in selenium_cookies:
            cookies[cookie['name']] = cookie['value']
        return cookies

    def __getHeaders(self):
        return self.driver.execute_script("return navigator.userAgent")

    def checkLogin(self):
        self.setup()
        outcome = self.__login()
        self.quit()
        return outcome
    
    def getTextBooks(self, path):
        self.setup()
        self.__login()

        textbookElements = self.__getTextBookElements()
        for textbook in textbookElements:
            # makes text book directory if it does not already exist
            try:
                os.makedirs(os.path.join(path,str(textbook.text).removeprefix("Loading...\n").replace("\n", " - ")))
            except FileExistsError:
                pass
            coverImage = requests.get(url=textbook.find_element(By.CLASS_NAME, "prodImage").get_attribute('src'), headers={"User-Agent":self.__getHeaders()}, cookies=self.__getCookies(), allow_redirects=True)
            coverPath = os.path.join(path,str(textbook.text).removeprefix("Loading...\n").replace("\n", " - "),"cover.png")
            
            # compare image on the web to image already downloaded
            if os.path.isfile(coverPath):
                with open(coverPath, "rb") as cover:
                    existingCover = cover.read()
                    cover.close()
                if existingCover != coverImage.content:
                    with open(coverPath, 'wb') as cover:
                        cover.write(coverImage.content)
                        cover.close()
            # just writes image if it does not already exist
            else: 
                with open(coverPath, 'wb') as cover:
                    print(3)
                    cover.write(coverImage.content)
                    cover.close()
        self.quit()
        return textbookElements
        

if __name__ == '__main__':
    path = os.path.join(os.path.dirname(__file__), "testFolderDeleteAfter")
    test = myNelson(profile={"browser":"","email":"","password":""}, browser="", logLevel=3)
    print(path)
    # print(test.checkLogin())
    print(test.getTextBooks(path=path))
