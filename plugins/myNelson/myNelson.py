import pathlib

from .lib.webScraper import *

plugName = pathlib.Path(__file__).stem

"""
function to test login credentials (login and returns true)

function to get textbooks on the side (login and once in gets list of textbooks)
    function to get textbook cover if exists updates every time

function to download textbook off site

function to merge pdf

function to make profile
"""

class autoForm(baseChromeWebScraper):
    def __init__(self, modules, profile, url:str = None, webDriverPath:str = "./chromedriver", autoWebDriverModule:str = "lib.autoChromeDriver", browser:str = None, browserDownloadPath:str = None, browserHide:str = False, userAgent:str = None, logLevel: int = None):
        self.modules = modules
        self.profile = profile
        super().__init__(url, webDriverPath, autoWebDriverModule, browser, browserDownloadPath, browserHide, userAgent, logLevel)

    def run(self):
        module = self.modules[[importedModule.plugName for importedModule in self.modules].index(self.profile["id"])]
        self.url = module.form
        self.setup()
        module.fillForm(self, self.profile)