import os, re, datetime, hashlib, pickle
from flask import render_template
from nJoyPorn import database, modules

userPattern = "{\"username\":\"(.*)\";\"password\":\"(.*)\";\"email\":\"(.*)\";\"id\":\"(.*)\";\"nickName\":\"(.*)\";\"role\":\"(.*)\"}"

userObjectList = []
userPageObjectList = []

def Run():
    command = input("Enter command [-initdb -newUser -deleteUser -editUser -editUserPage \n               -printPageList -printVideoList -printUsers -printFavorites -printPurchased]: ")
    if command == "-initdb":
        InitDB()
        Run()
    if command == "-newUser":
        InitDB()
        username = database.userDatabase.CreateMD5Hash(input("Enter username: "))
        password = database.userDatabase.CreateMD5Hash(input("Enter password: "))
        email = input("Enter email: ")
        nickName = input("Enter nick name: ")
        role = input("Enter user role: [user, admin]")
        CreateUser(username, password, email, nickName, role)
    if command == "-editUser":
        InitDB()
        EditUser()
    if command == "-deleteUser":
        InitDB()
        print("Enter clear name and password")
        username = database.userDatabase.CreateMD5Hash(input("Enter username: "))
        password = database.userDatabase.CreateMD5Hash(input("Enter password: "))
        if CheckCredentials(username, password) == True:
            global userObjectList
            for user in userObjectList:
                if user.username == username and user.password == password:
                    userObjectList.remove(user)
                    SaveUserDatabase()
    if command == "-printUsers":
        Api_Call_LoadFullUsersList()
        PrintUsers()                
    if command == "-printVideoList":
        InitDB()
        command = input("Leaf blank to print all users or\nEnter user-id: ")
        if command == "":
            PrintAllUsersVideoList()
        else:
            PrintUserVideoList(command)
    if command == "-printFavorites":
        InitDB()
        command = input("Enter user-id: ")
        PrintUserFavoriteVideoList(command)
    if command == "-printPurchased":
        InitDB()
        command = input("Enter user-id: ")
        PrintUserPurchasedVideoList(command)
    if command == "-printPageList":
        InitDB()
        LoadFullUserPageList()
        PrintUserPageList()
    if command == "-editUserPage":
        InitDB()
        LoadFullUserPageList()
        EditUserPage()        
    return None

def LoadUserFromDatabase(_username):
    global userObjectList
    for user in userObjectList:
        if user.username == _username:
            return user
    return "invalid"
        
def LoadUserObjectByName(_username):
        global userObjectList
        for user in userObjectList:
            if user.username == _username:
                userObject = pickle.load(open(os.getcwd()+"/userDatabase/" + _username + "/userdata", "rb"))
                return userObject

def LoadUserObjectById(_id):
    global userObjectList
    for user in userObjectList:
        if user.id == _id:
            userObject = pickle.load(open(os.getcwd()+"/userDatabase/" + user.username + "/userdata", "rb"))
            return userObject
               
def LoadUserDatabase():
    InitDB()

def Api_Call_LoadFullUsersList():
    InitDB()
    global userObjectList
    tempList = []
    for userObject in userObjectList:
        tempList.append(LoadUserObjectById(userObject.id))
    userObjectList.clear()
    userObjectList = tempList.copy()

def InitDB():
    if os.path.exists(os.getcwd()+"/userDatabase/userDatabase.db"):
        file = open(os.getcwd()+"/userDatabase/userDatabase.db" ,"r")
        lines = file.readlines()
        global userObjectList
        userObjectList.clear()
        for line in lines:
            userObjectList.append(LineToUserObject(line))
        print("USERDATABASE: database loaded")
        return
    print("USERDATABASE: You have to create a userDatabase.db file @: " + os.getcwd()+"/userDatabase/")
    return


def EditUser():
    id = input("Enter userId: ")
    userObject = LoadUserObjectById(id)
    if userObject == "invalid":
        print("User not found")
    password = input("Enter a new password: ")
    if password != "":
        userObject.password = CreateMD5Hash(password)
        print("New password: " + password)
    role = input("Enter new role: ")
    if role != "":
        userObject.role = role
        print("New role: " + userObject.role)
    command = input("Clear video-List: ")
    if command == "yes":
        userObject.videoList.clear()
    command = input("Add video to videoList? ")
    if command == "yes":
        run = True
        while run:
            videoId = input("Enter video id: ")
            if videoId == "":
                run = False
                break
            userObject.videoList.append(videoId)
    command = input("Something else? ")
    if command == "-clearFollowerList":
        userObject.followerList.clear()
    UpdateWrittenUserObjectInDatabase(userObject)
    SaveUserData(userObject)
    SaveUserDatabase()
    Run()

def GetUserNameList():
    return os.listdir(os.getcwd()+"/userDatabase/")

def GetSupportUserObject():
    global userObjectList
    for userObject in userObjectList:
        if userObject.role == "support":
            return userObject

def LineToUserObject(_line):
    userObject = database.modules.User()
    result = re.search(userPattern, _line)
    userObject.username = result.group(1)
    userObject.password = result.group(2)
    userObject.email = result.group(3)
    userObject.id = result.group(4)
    userObject.nickName = result.group(5)
    userObject.role = result.group(6)
    return userObject

def UserObjectToLine(_userObject):
    line = "{\"username\":\"" + _userObject.username + "\";\"password\":\"" + _userObject.password + "\";\"email\":\"" + _userObject.email + "\";\"id\":\"" + _userObject.id + "\";\"nickName\":\"" + _userObject.nickName + "\";\"role\":\"" + _userObject.role + "\"}"
    return line

def SaveUserDatabase():
    global userObjectList
    lines = []
    for user in userObjectList:
        lines.append(UserObjectToLine(user)+"\n")
    userDatabaseFile = open(os.getcwd()+"/userDatabase/userDatabase.db", "w")
    userDatabaseFile.writelines(lines)
    print("USERDATABASE: User database saved")
    
def SaveUserData(_userObject):
    file = open(os.getcwd()+"/userDatabase/"+_userObject.username+"/userdata", "wb")
    pickle.dump(_userObject, file)
    file.close()
    LoadUserDatabase()
    print("USERDATABASE: User list reloaded")

def UpdateWrittenUserObjectInDatabase(_userObject):
    userLine = UserObjectToLine(_userObject)
    userDatabaseFile = open(os.getcwd()+"/userDatabase/userDatabase.db", "r")
    lines = userDatabaseFile.readlines()
    userDatabaseFile.close()
    for line in lines:
        if _userObject.id in line:
            print("DEBUG userdatabase line: " + line)
            lines.remove(line)
            lines.append(userLine)
    userDatabaseFile = open(os.getcwd()+"/userDatabase/userDatabase.db", "w")
    userDatabaseFile.writelines(lines)
    userDatabaseFile.close()
        
        
def WriteUserToDatabase(_line):
    file = open(os.getcwd()+"/userDatabase/userDatabase.db", "a")
    file.write(_line+"\n")
    print("USERDATABASE: User written to database")

def CreateUser(_username, _password, _email, _nickName, _role):
    id = CreateRandomId()
    line = "{\"username\":\"" + _username + "\";\"password\":\"" + _password + "\";\"email\":\"" + _email + "\";\"id\":\"" + id + "\";\"nickName\":\"" + _nickName + "\";\"role\":\"" + _role + "\"}"
    WriteUserToDatabase(line)
    os.mkdir(os.getcwd()+"/userDatabase/"+_username)
    os.mkdir(os.getcwd()+"/userDatabase/"+_username+"/messages")
    CreateUserObject(_username, _password, _email, id, _nickName, _role)
    return True

def CreateUserObject(_username, _password, _email, _id, _nickName, _role):
    global userObjectList
    user = modules.User()
    user.username = _username
    user.password = _password
    user.email = _email
    user.id = _id
    user.nickName = _nickName
    user.role = _role
    userObjectList.append(user)
    SaveUserData(user)

def EditUserPage():
    LoadFullUserPageList()
    global userPageObjectList
    pageId = input("Enter page-Id: ")
    for userPageObject in userPageObjectList:
        if userPageObject.id == pageId:
            nickName = input("Enter nickname: ")
            if nickName != "":
                userPageObject.nickName = nickName
            discription = input("Enter user discription: ")
            if discription != "":
                userPageObject.userDiscription = discription
            catchPhrase = input("Enter catch phrase: ")
            if catchPhrase != "":
                userPageObject.catchPhrase = catchPhrase
            command = input("Edit categories? [yes / no] ")
            if command == "yes":
                categorieString = ""
                for categorie in userPageObject.categorieList:
                    if categorieString != "":
                        categorieString += ", " + categorie
                    if categorieString == "":
                        categorieString += categorie
                print("Categorie-List: " + categorieString)
                command = input("-add, -remove, -replace: ")
                if command == "-add":
                    categories = re.split("\,", input("Enter categorie name: "))
                    for categorie in categories:
                        userPageObject.categorieList.append(categorie)
                if command == "-remove":
                    categorie = input("Enter categorie: ")
                    try:
                        userPageObject.categorieList.remove(categorie)    
                    except:
                        print("Categorie not found")
                if command == "-replace":
                    categorie = input("Enter categorie you want to replace replace: ")
                    try:
                        userPageObject.categorieList.remove(categorie)
                        newCategorie = input("Enter new categorie: ")
                        userPageObject.categorieList.append(newCategorie)    
                    except:
                        print("Categorie not found")
            SaveUserPageData(userPageObject)
    
def GetUserPageObjectByPageId(_pageId):
    global userPageObjectList
    for userPageObject in userPageObjectList:
        if userPageObject.id == _pageId:
            return userPageObject
    return "invalid"
    

def SearchInUserVideos(_pageId, _searchTerm):
    userPageObject = GetUserPageObjectByPageId(_pageId)
    tempList = userPageObject.videoList.copy()
    resultList = []
    gotcha = False
    if _searchTerm == "":
        return tempList
    for metaInformationObject in tempList:
        if _searchTerm in metaInformationObject.videoTitle and gotcha == False:
            gotcha = True
            resultList.append(metaInformationObject)
            tempList.remove(metaInformationObject)
        if gotcha == False:
            for tag in metaInformationObject.tagList:
                if tag in _searchTerm:
                    gotcha = True
                    resultList.append(metaInformationObject)
                    tempList.remove(metaInformationObject)
                    break
        gotcha = False
    return resultList


def SetupUserPage(_nickName, _username, _discription, _catchPhrase, _categories):
    userObject =  GetUserByName(_username)
    userPageObject = modules.UserPageData()
    userPageObject.username = _username
    userPageObject.userDiscription = _discription
    userPageObject.userId = userObject.id
    userPageObject.nickName = _nickName
    userPageObject.catchPhrase = _catchPhrase
    userPageObject.categorieList = re.split(",", _categories)
    userPageObject.id = CreateRandomId()
    imagePathList = []
    imageFileList = os.listdir(os.getcwd()+"/data/userPages/"+_username+"/images/")
    if len(imageFileList) > 0:
        for image in imageFileList:
            imagePathList.append("/data/userPages/"+_username+"/images/"+image)
        userPageObject.profilePicturePath = imagePathList[0]
        userPageObject.picturePathList = imagePathList
    global userPageObjectList
    userPageObjectList.append(userPageObject)
    SaveUserPageData(userPageObject)
    return userPageObject
              
def UpdateUserPictures(_id, _username):
    userPageObject = GetUserPageDataByUserId(_id)
    print(userPageObject.userName)
    imagePathList = []
    imageFileList = os.listdir(os.getcwd()+"/data/userPages/"+_username+"/images/")
    if len(imageFileList) > 0:
        for image in imageFileList:
            imagePathList.append("/data/userPages/"+_username+"/images/"+image)
        userPageObject.profilePicturePath = imagePathList[0]
        userPageObject.picturePathList = imagePathList
        SaveUserPageData(userPageObject)
    return userPageObject

def RemoveUserPagePicture(_picturePath, _userId):
    userPageObject = GetUserPageDataByUserId(_userId)
    for picturePath in userPageObject.picturePathList:
        if picturePath == _picturePath:
            userPageObject.picturePathList.remove(picturePath)
            SaveUserPageData(userPageObject)
            os.remove(os.getcwd()+_picturePath)
            return userPageObject
    return "invalid"
          
def SaveUserPageData(_userPageData):
    file = open(os.getcwd()+"/userDatabase/"+_userPageData.username+"/userPageData", "wb")
    pickle.dump(_userPageData, file)
    file.close()
    print("USERDATABASE: User-Page for user named: " + _userPageData.username + " saved")

def AddMetaInformationObjectsToUserPageObjectVideoList(_userPageObject):
    print("try get video mios")
    videoMetaInformationObjectList = []
    userObject = LoadUserObjectById(_userPageObject.userId)
    for videoId in userObject.videoList:
        print("wanna get that mio: ", videoId)
        videoMetaInformationObjectList.append(database.GetMetaInformationObjectById(videoId))
    _userPageObject.videoList.clear()
    videoMetaInformationObjectList = database.ExcludeTrailerObjects(videoMetaInformationObjectList)
    _userPageObject.videoList = videoMetaInformationObjectList.copy()
    return _userPageObject
    
def GetUserPageDataByUserId(_userId):
    if _userId == "robot.txt":
        print("Bot detected")
        return "invalid"
    global userPageObjectList
    print("lenlist: " + str(len(userPageObjectList)))
    for userPageObject in userPageObjectList:
        if userPageObject.userId == _userId:
            #userPageObject = ReformatPageDiscriptionText(userPageObject)
            return userPageObject
    return LoadUserPageDataByUserId(_userId)

def GetUserPageDataByUserNickName(_nickName):
    print("DEBGU: _nickName >> " + _nickName)
    if _nickName == "robot.txt":
        print("Bot detected")
        return "invalid"
    global userObjectList
    for userObject in userObjectList:
        if userObject.nickName == _nickName:
            return LoadUserPageDataByUserId(userObject.id)
    return "invalid"

def ReformatPageDiscriptionText(_userPageObject):
    # _userPageObject.userDiscription = re.sub("&lt;","<",_userPageObject.userDiscription)
    # _userPageObject.userDiscription = re.sub("&gt;","<",_userPageObject.userDiscription)
    # _userPageObject.userDiscription = re.sub("&amp;#10084;", "&#9829;",_userPageObject.userDiscription)
    # _userPageObject.userDiscription = re.sub("<br>","\n",_userPageObject.userDiscription)
    return _userPageObject

#i am not willing to populate the list fully on start
# def GetUserPageDataByPageId(_pageId):
#     global userPageObjectList
#     for userPageObject in userPageObjectList:
#         if userPageObject.id == _pageId:
#             return userPageObject
#     return "invalid"

def LoadUserPageDataByUserId(_userId):
    global userPageObjectList
    userObject = LoadUserObjectById(_userId)
    try:
        file = open(os.getcwd()+"/userDatabase/"+userObject.username+"/userPageData", "rb")
        userPageObject = pickle.load(file)
        userPageObjectList.append(userPageObject)
        return userPageObject
    except:
        print("USERDATABASE: User page not found. Does the file exist?")
        return "invalid"

def LoadFullUserPageList():
    global userObjectList
    for userObject in userObjectList:
        LoadUserPageDataByUserId(userObject.id)
    return None

def RemoveUserFromListById(_id, _password):    
    global userObjectList
    userObject = GetUserById(_id)
    if userObject == "invalid":
        return False
    if userObject.password == _password:
        userObjectList.remove(userObject)
        os.remove(os.getcwd()+"/userDatabase/"+userObject.username+"/userData")
        os.rmdir(os.getcwd()+"/userDatabase/"+userObject.username)
        SaveUserDatabase()
        return True
    return False
        
def CreateRandomId():
    return hashlib.md5(str(datetime.datetime.now()).encode()).hexdigest()

def CreateMD5Hash(_input):
    return hashlib.md5(_input.encode()).hexdigest()

def CheckCredentials(_username, _password):
    global userObjectList
    for user in userObjectList:
        if user.username == _username and user.password == _password:
            return True
    return False

def GetUserList():
    return userObjectList

def GetUserById(_id):
    global userObjectList
    print("DEBUG: userObjectList|len >> " + str(len(userObjectList)) + " _id >> " + _id)
    for userObject in userObjectList:
        if userObject.id == _id:
            print("DEBUG:userObject.username >> " + userObject.username)
            return userObject
    return "invalid"

def GetUserByCredentials(_username, _password):
    global userObjectList
    for userObject in userObjectList:
        if userObject.username == _username and userObject.password == _password:
            userObject = LoadUserObjectByName(_username)
            userObject.videoList = database.GetUserVideoList(userObject.id)
            userObject.favoriteList = database.GetUserFavoriteList(userObject.id)
            userObject.purchasedVideosList = database.GetUserPurchasedVideosList(userObject.id)
            return userObject
    return "invalid"

def GetUserByName(_username):
    global userObjectList
    for userObject in userObjectList:
        if userObject.username == _username:
            return userObject

def UpdateUserVideoList(_username, _videoId):
    userObject = LoadUserObjectByName(_username)
    userObject.videoList.append(_videoId)
    SaveUserData(userObject)
    
def PrintAllUsersVideoList():
    global userObjectList
    userVideoListString = ""
    for user in userObjectList:
        userObject = LoadUserObjectById(user.id)
        for videoId in userObject.videoList:
            if userVideoListString != "":
                userVideoListString += ", " + videoId
            if userVideoListString == "":
                userVideoListString = videoId
        print("User-ID: " + user.id + "\nVideo-Id List: "+userVideoListString)        
        userVideoListString = ""

def PrintUserVideoList(_id):
    global userObjectList
    userVideoListString = ""
    for user in userObjectList:
        if user.id == _id:
            userObject = LoadUserObjectById(user.id)
            for videoId in userObject.videoList:
                if userVideoListString != "":
                    userVideoListString += ", " + videoId
                if userVideoListString == "":
                    userVideoListString = videoId
            print("User-ID: " + user.id + "\nVideo-Id List: "+userVideoListString)        
            userVideoListString = ""
            
def PrintUserFavoriteVideoList(_id):
    global userObjectList
    userVideoListString = ""
    user = LoadUserObjectById(_id)
    for videoId in user.favoriteList:
        if userVideoListString != "":
            userVideoListString += ", " + videoId
        if userVideoListString == "":
            userVideoListString = videoId
    print("User-ID: " + user.id + "\nVideo-Id List: "+userVideoListString)        
    userVideoListString = ""

def PrintUserPurchasedVideoList(_id):
    global userObjectList
    userPurchasedVideosListString = ""
    user = LoadUserObjectById(_id)
    for videoId in user.purchasedVideosList:
        if userPurchasedVideosListString != "":
            userPurchasedVideosListString += ", " + videoId
        if userPurchasedVideosListString == "":
            userPurchasedVideosListString = videoId
    print("User-ID: " + user.id + "\nVideo-Id List: "+userPurchasedVideosListString)        
    userPurchasedVideosListString = ""

def PrintUserPageList():
    global userPageObjectList
    for userPageObject in userPageObjectList:
        categorieListString = ""
        for categorie in userPageObject.categorieList:
            if categorieListString != "":
                categorieListString += ", " + categorie
            if categorieListString == "":
                categorieListString += categorie
        picturePathListString = ""
        for picturePath in userPageObject.picturePathList:
            if picturePathListString != "":
                picturePathListString += ", " + picturePath
            if picturePathListString == "":
                picturePathListString += picturePath    
        print("Page-Id: " + userPageObject.id + "\nUser-Id: " + userPageObject.userId + "\nNick-Name: " + userPageObject.nickName + "\nCatch-Phrase: " + userPageObject.catchPhrase + "\nCategorie-List: " + categorieListString +"\nPicturePath-List: " + picturePathListString +"\n")
        categorie = ""
        
def PrintUsers():
    global userObjectList
    for userObject in userObjectList:
        followerString = ""
        for follower in userObject.followerList:
            if followerString != "":
                followerString += ", " + follower
            if followerString == "":
                followerString += follower
        print("User-Name: " + userObject.username+"\nUser-Password: " + userObject.password+"\nUser-ID: " + userObject.id + "\nRole : " + userObject.role+"\nUser-ID: " + "\nUser-Follower: " + str(len(userObject.followerList)))

def AddItemToCard(_videoId, _username, _password):
    userObject = GetUserByCredentials(_username, _password)
    if userObject == "invalid":
            return render_template("error.html", error=modules.ErrorMessage("Video not addet to card", "Something went wrong"))
    if VideoIsInUserCardList(userObject.cardList, _videoId) == False:
        userObject.cardList.append(_videoId)
        return userObject
    return render_template("error.html", error=modules.ErrorMessage("Video allready in card", "You added this video allready to your card"))
    
def VideoIsInUserCardList(_cardList, _videoId):
    for videoId in _cardList:
        if videoId == _videoId:
            return True
    return False
        
def RemoveVideoFromCard(_userId, _videoId):
    userObject = GetUserById(_userId)
    for videoId in userObject.cardList:
        if videoId == _videoId:
            userObject.cardList.remove(videoId)
            return userObject.cardList
    return "invalid"

def AddVideoToUserFavoriteList(_videoId, _userId):
    userObject = GetUserById(_userId)
    fullUserObject = LoadUserObjectById(_userId)
    userObject = fullUserObject
    userObject.favoriteList.append(_videoId)
    SaveUserData(userObject)
    userObject.favoriteList = database.GetUserFavoriteList(_userId)
    return None

def RemoveFavoriteFromList(_userId, _videoId):
    userObject = GetUserById(_userId)
    fullUserObject = LoadUserObjectById(_userId)
    userObject = fullUserObject
    for videoId in userObject.favoriteList:
        if videoId == _videoId:
            userObject.favoriteList.remove(videoId)
    SaveUserData(userObject)
    userObject.favoriteList = database.GetUserFavoriteList(_userId)

#for testing only    
def AddVideoToPurchasedList(_userId, _videoId):
    userObject = GetUserById(_userId)
    fullUserObject = LoadUserObjectById(_userId)
    userObject = fullUserObject
    userObject.purchasedVideosList.append(_videoId)
    SaveUserData(userObject)
    userObject.purchasedVideosList = database.GetUserPurchasedVideosList(_userId)
    return None

def UserHasPurchasedVideo(_userId, _videoId):
    userObject = LoadUserObjectById(_userId)
    for purchasedVideoId in userObject.purchasedVideosList:
        if purchasedVideoId == _videoId:
            return True
    return False

def UserCanConnectSellVideoToTrailer(_trailerId, _userId):
    trailerObject = database.GetMetaInformationObjectById(_trailerId)
    userObject = LoadUserObjectById(_userId)
    try:
        print(userObject.id)
    except Exception as e:
        print(e)
    if trailerObject.owner == userObject.id:
        return True
    return False

def UserExists(_username):
    global userObjectList
    for userObject in userObjectList:
        if userObject.username == _username:
            return True
    return False
    
######################## W E B G U I - I M P L E M E N T A T I O N ########################
#
def Modules_UserObject():
    advancedUserObject = modules.User()
    userObject = GetUserById("id")
    
def From_GUI_AddUser(_username, _password, _email, _nickName):
    if UserExists(_username):
        return "<script>alert(\"User allready exists in userDatabase.\");location.href = \"webgui\";</script>"
    CreateUser(_username, _password, _email, _nickName, "user")
    return "<script>alert(\"User successfully addet to the userDatabase.\");location.href = \"webgui\";</script>"

def From_GUI_AddRandomUser(_username, _password, _email, _nickName):
    if UserExists(_username):
        return "<script>alert(\"User allready exists in userDatabase.\");location.href = \"webgui\";</script>"
    CreateUser(_username, _password, _email, _nickName, "randomUser")
    return "<script>alert(\"Your registration is complete you can now login.\");location.href = \"login\";</script>"

def From_GUI_EditUser(_id, _username, _password, _email, _nickName, _currentPassword, _role):
    userObject = GetUserById(_id)
    if userObject == "invalid":
        return render_template("error.html", error=modules.ErrorMessage("User not edited", "Please check the id or password you entered"))
    if userObject.password != _currentPassword:
        return render_template("error.html", error=modules.ErrorMessage("User not edited", "Please check the id or password you entered"))
    if _username != "":
        userObject.username = _username
    if _password != "":
        userObject.password = _password
    if _email != "":
        userObject.email = _email
    if _nickName != "":
        userObject.nickName = _nickName
    if _role != "":
        userObject.role = _role
    SaveUserDatabase()
    return "<script>alert(\"User successfully edited and saved to the userDatabase.\");location.href = \"webgui\";</script>"

def From_GUI_EditAccount(_id, _username, _password, _email, _nickName, _currentPassword):
    userObject = GetUserById(_id)
    if userObject == "invalid":
        return render_template("error.html", error=modules.ErrorMessage("User not edited", "Please check the id or password you entered"))
    if userObject.password != _currentPassword:
        return render_template("error.html", error=modules.ErrorMessage("User not edited", "Please check the id or password you entered"))
    if _username != "":
        userObject.username = _username
    if _password != "":
        userObject.password = _password
    if _email != "":
        userObject.email = _email
    if _nickName != "":
        userObject.nickName = _nickName
    SaveUserDatabase()
    return "<script>alert(\"User successfully edited and saved to the userDatabase.\");location.href = \"userAccount\";</script>"

def From_GUI_ResetPassword(_id, _username, _password):
    global userObjectList
    print("USERDATABASE: reset password for id = " + _id)
    for userObject in userObjectList:
        if userObject.id == _id and userObject.username == _username:
            if userObject.role == "admin":
                return render_template("error.html", error=modules.ErrorMessage("Is it realy you?", "If yes I am sorry but get your ass to a terminal"))
            userObject.password = _password
            SaveUserDatabase()
            LoadUserDatabase()
            return "<script>alert(\"Password succesfully resettet. You can now login with your new password.\");location.href = \"login\";</script>"
    return render_template("error.html", error=modules.ErrorMessage("User not found", "Can't find the user :/"))    
        
def From_GUI_RemoveUser(_id, _password):
    if RemoveUserFromListById(_id, _password):
        return "<script>alert(\"User successfully removed from to the userDatabase.\");location.href = \"webgui\";</script>"
    return render_template("error.html", error=modules.ErrorMessage("User not removed", "Please check the id or password you entered"))         

def From_GUI_HasPrivileges(_username, _password):
    global userObjectList
    for user in userObjectList:
        if user.username == _username and user.password == _password:
            if user.role == "admin":
                return 1000
            if user.role == "support":
                return 112
            if user.role == "user":
                return 12
            if user.role == "randomUser":
                return 11
            if user.role == "verified":
                return 21
    return 0

def From_GUI_CheckForPossiblePasswordResett(_username, _nickName, _email):
    userObject = LoadUserFromDatabase(_username)
    if userObject == "invalid":
        return render_template("error.html", error=modules.ErrorMessage("Permission denied", "You entered a wrong username, nickname, email combination"))
    if userObject.nickName == _nickName or userObject.email == _email:
        return render_template("resettPassword.html", id=userObject.id, username=userObject.username)
    return render_template("error.html", error=modules.ErrorMessage("Permission denied", "You entered a wrong username, nickname, email combination"))

def From_GUI_EditUserPage(_userId, _nickName, _username, _userDiscription, _catchPharse, _categories):
    userPageObject = GetUserPageDataByUserId(_userId)
    nickName = _nickName
    if nickName != "":
        userPageObject.nickName = nickName
    discription = _userDiscription
    if discription != "":
        userPageObject.userDiscription = discription
    catchPhrase = _catchPharse
    if catchPhrase != "":
        userPageObject.catchPhrase = catchPhrase
    categories = re.split("\,", _categories)
    if len(categories) > 1:
        userPageObject.categorieList = categories
    imagePathList = []
    imageFileList = os.listdir(os.getcwd()+"/data/userPages/"+_username+"/images/")
    if len(imageFileList) > 0:
        for image in imageFileList:
            imagePathList.append("/data/userPages/"+_username+"/images/"+image)
        userPageObject.profilePicturePath = imagePathList[0]
        userPageObject.picturePathList = imagePathList
    SaveUserPageData(userPageObject)
    return userPageObject        

def From_GUI_FollowUser(_userToFollowId, _newFollowerId):
    print("DEBUG: Follower")
    userToFollow = LoadUserObjectById(_userToFollowId)
    if _newFollowerId in userToFollow.followerList:
        return
    newFollowerObject = LoadUserObjectById(_newFollowerId)
    userToFollow.followerList.append(_newFollowerId)
    newFollowerObject.followingList.append(_userToFollowId)
    for follower in userToFollow.followerList:
        print("Followers: " + follower)
    SaveUserData(userToFollow)
    SaveUserData(newFollowerObject)
    return

##################################### H E L P E R #####################################
#
# def UpgradeUserObject():
#     InitDB()
#     #Api_Call_LoadFullUsersList
#     global userObjectList
#     newUserObjectList = []
#     for userObject in userObjectList:
#         #newUserObject = modules.NewUserObject()
#         newUserObject = modules.User()
#         newUserObject.username = userObject.username
#         newUserObject.password = userObject.password
#         newUserObject.email = userObject.email
#         newUserObject.favoriteList = userObject.favoriteList
#         newUserObject.loginStampList = userObject.loginStampList
#         newUserObject.videoList = userObject.videoList
#         newUserObject.id = userObject.id
#         newUserObject.nickName = userObject.nickName
#         newUserObject.role = userObject.role
#         newUserObject.cardList = userObject.cardList
#         newUserObject.purchasedVideosList = userObject.purchasedVideosList
#         newUserObject.followerList = []
#         newUserObject.followingList = []
#         newUserObjectList.append(newUserObject)
#     userObjectList.clear()
#     userObjectList = newUserObjectList.copy()
#     for user in userObjectList:
#         SaveUserData(user)
    
if __name__ == "__main__":
    Run()