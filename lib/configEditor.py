import json, sys, os, shutil

configJson = "config.json"

def gen():
    baseConfig = {
        "browserPath":"",
        "users":{}
    }
    with open(os.path.join(sys.path[0],configJson), "w") as confFile:
        confFile.write(json.dumps(baseConfig, indent=4))
    os.makedirs(os.path.join(sys.path[0],"users"))

def editBrowserPath(browserPath: str):
    data: dict
    with open(os.path.join(sys.path[0],configJson), "r") as confFile: # 
        data = json.load(confFile)
    if os.path.isfile(browserPath):
        data["browserPath"] = browserPath
        with open(os.path.join(sys.path[0],configJson), "w") as confFile:
            confFile.write(json.dumps(data, indent=4))
    else:
        raise Exception('Browser path is not a valid file path: ' + browserPath)

def getBrowserPath():
    with open(os.path.join(sys.path[0],configJson), "r") as confFile: # 
        return str(json.load(confFile)["browserPath"])

def listUsers():
    with open(os.path.join(sys.path[0],configJson), "r") as confFile: # 
        return list(json.load(confFile)["Users"].keys())

def userAdd(username: str, password: str, name: str = None):
    data: dict
    with open(os.path.join(sys.path[0],configJson), "r") as confFile: # 
        data = json.load(confFile)
    data["users"].update({(username if name == None else name):{"email": username, "password": password}})
    with open(os.path.join(sys.path[0],configJson), "w") as confFile:
        confFile.write(json.dumps(data, indent=4))
    os.makedirs(os.path.join(sys.path[0],"users",(username if name == None else name)))

def userDelete(name: str):
    try:
        shutil.rmtree(os.path.join(sys.path[0],"users",name))
        data: dict
        with open(os.path.join(sys.path[0],configJson), "r") as confFile: # 
            data = json.load(confFile)
        data["users"].pop(name)
        with open(os.path.join(sys.path[0],configJson), "w") as confFile:
            confFile.write(json.dumps(data, indent=4))
    except OSError as e:
        print("Error: %s - %s." % (e.filename, e.strerror))

def userEdit(name: str, newEmail: str = None, newPassword: str = None, newName: str = None):
    data: dict
    with open(os.path.join(sys.path[0],configJson), "r") as confFile: # 
        data = json.load(confFile)
    if newEmail:
        data["users"][name]["email"] = newEmail
    if newPassword:
        data["users"][name]["password"] = newEmail
    if newName:
        data["users"][newName] = data["users"].pop(name)
        os.rename(os.path.join(sys.path[0],"users",name), os.path.join(sys.path[0],"users", newName))
    with open(os.path.join(sys.path[0],configJson), "w") as confFile:
        confFile.write(json.dumps(data, indent=4))    