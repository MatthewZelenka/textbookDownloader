def login(self, profile, pageProcedure:list=[], printOut=False):
    while True: # runs every url to see if one of the protocols can solve the page if not then assume login is over and exits
        currentUrl = self.driver.current_url
        for procedure in pageProcedure:
            if currentUrl.find(procedure.url) != -1:
                process = procedure.doPage(self, profile)
                if printOut: print(process)
                break
            elif procedure == pageProcedure[-1]:
                return True
        self.waitUrlChange(currentURL=currentUrl, waitTime=2)