import pip, os, sys, requests, zipfile
while True:
    try:
        from bs4 import BeautifulSoup, SoupStrainer
        from urllib.request import Request, urlopen
        break
    except:
        if __name__ == '__main__':
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
        else:
            raise

def autoInstall(browserPath = None):
    def getLinkFromKeyword(site, keyword): #gets chrome driver version link from the site and current version of browser
        req = Request(site)
        html_page = urlopen(req) # gets webpage data

        soup = BeautifulSoup(html_page, features="lxml", parse_only=SoupStrainer('a')) # into bs object

        links = []
        for link in soup.findAll('a'): # goes throught all the links in the html file and gets the ones with the keyword
            if keyword in str(link.get('href')):
                links.append(link.get('href'))
        return links[0] # returns first instance as it is probably 99% of the time the correct link
    
    def downloadDriver(downloadPage: str, osType): # gets driver version then inserts it in to the download link for supported os
        downloadUrlBase = "https://chromedriver.storage.googleapis.com/"
        osTypeToDriverZip = {
            "win32":"chromedriver_win32.zip",
            "linux":"chromedriver_linux64.zip"
        }
        url = downloadUrlBase+downloadPage[downloadPage.find("path=")+5:]+osTypeToDriverZip[osType] # the combining
        r = requests.get(url, allow_redirects=True)
        open(os.path.join(sys.path[0], osTypeToDriverZip[osType]), 'wb').write(r.content)
        return os.path.join(sys.path[0], osTypeToDriverZip[osType])

    def extractDriver(filePath):
        with zipfile.ZipFile(filePath, 'r') as zip_ref:
            zip_ref.extractall(os.path.dirname(filePath))
            zip_ref.close()
        os.remove(filePath)

    chromeDriverSite = "https://chromedriver.chromium.org/downloads"
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
            version = os.popen("wmic datafile where 'name=\""+browserPath.replace("\\", "\\\\").replace("/", "\\\\")+"\"' get version").read().splitlines()[2]
            extractDriver(downloadDriver(downloadPage=getLinkFromKeyword(site=chromeDriverSite, keyword=version.split(".")[0]), osType=sys.platform))
            # wmic datafile where 'name="C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe"' get version
        else:
            print("Automatic drivers unable to be downloaded for Windows "+str(sys.getwindowsversion().major)+" go to \""+chromeDriverSite+"\" to download manually for your chrome based browser and put in the folder \""+os.path.dirname(__file__)+"\"")
    else:
        print("Automatic drivers unable to be downloaded for "+sys.platform+" go to \""+chromeDriverSite+"\" to download manually for your chrome based browser and put in the folder \""+os.path.dirname(__file__)+"\"")

if __name__=="__main__":
    autoInstall(browserPath = "C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe")