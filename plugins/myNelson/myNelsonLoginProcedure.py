from lib.webScraper import *
from dataclasses import dataclass

@dataclass
class myNelsonLoginPage:
    url = "https://www.mynelson.com/mynelson/staticcontent/html/PublicLogin.html"
    def doPage(self, profile) -> str:
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, "txt-clear")))
        self.driver.find_element(By.ID, "txt-clear").click()
        self.driver.find_element(By.ID, "txtUName").send_keys(profile["email"])
        # Clicks and inputs password
        self.driver.find_element(By.ID, "password-clear").click()
        self.driver.find_element(By.ID, "txtPwd").send_keys(profile["password"])
        # Clicks on login
        self.driver.find_element(By.ID, "btnLogin").click()
        return "Logged into My NELSON"