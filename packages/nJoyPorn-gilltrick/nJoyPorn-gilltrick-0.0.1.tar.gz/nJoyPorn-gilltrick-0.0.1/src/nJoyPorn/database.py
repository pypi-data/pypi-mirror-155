import os, re, cv2, pickle, datetime, hashlib, random, requests
from nJoyPorn import pornhubScraper, modules, fapsterScraper, userDatabase, analytics, hotexporntoonsScraper, communication
from flask import render_template
from fake_headers import Headers
from pathlib import Path


fullList = []
defaultMetaInformationList = []
metaInformationObjectList = []

categoryNameList = []
popularCategoriesList = []
pornStarList = []
popularPornStarList = []
userPageCategorieList = []
videoStoragePath = "/static/storage/specials/"
forSaleStoragePath = "/static/protected/videos/"
fileNamePattern = re.compile("<FileStorage:\s'(.*)'\s\('.*'\)")
dbPattern = "{\"videoTitle\":\"(.*)\"videoUrl\":\"(.*)\"videoImageUrl\":\"(.*)\"videoDuration\":\"(.*)\",\"directLink\":\"(.*)\",\"categoryName\":\"(.*)\",\"id\":\"(.*)\",\"videoLink\":\"(.*)\",\"tagList\":\[(.*)\],\"userTagList\":\[(.*)\],\"durationInSeconds\":(.*)}"
tagListPatter = "\w+|\s\w+"

pornhubMetaInformationObjectList = []
fapsterMetaInformationObjectList = []
hotexporntoonsMetaInformationObjectList = []


def GetVideoDuration(_videoUrl):
    data = cv2.VideoCapture(_videoUrl)
    frames = data.get(cv2.CAP_PROP_FRAME_COUNT)
    seconds = int(frames / 30)
    if frames <= 0:
        video_filename = os.getcwd()+_videoUrl
        cap = cv2.VideoCapture(video_filename)
        videoLength = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) - 1
        seconds = int(videoLength / 30)
    return seconds

def InitDatabase():
    LoadCategorieList()
    LoadPornStarNameList()
    LoadDB()
    global fullList
    LoadPornhubDB()
    print("DATABASE: PornHub database loaded")
    print("DATABASE: total record count in database : " + str(len(fullList)))
    LoadFapsterDB()
    print("DATABASE: Fapster database loaded")
    print("DATABASE: total record count in database : " + str(len(fullList)))
    #I have an error in my thumbnails the cdn is down :/
    #LoadHotExPornToonsDB()
    #print("DATABASE: HotExPornToons database loaded")
    #print("DATABASE: total record count in database : " + str(len(fullList)))
    userDatabase.InitDB()
    print("DATABASE: User database loaded")
    analytics.InitDB()
    print("DATABASE: Analytics database loaded")
    LoadUserPageCategorieList()


def LoadDB():
    global metaInformationObjectList
    global fullList
    file = open(os.getcwd()+"/data/databases/videoDatabase.db", "rb")
    try:
        metaInformationObjectList = pickle.load(file)
        print("DATABASE: nJoyPorn database loaded")
        print("DATABASE: total record count in database: " + str(len(metaInformationObjectList)))
    except:
        print("DATABASE: nJoyPorn database not loaded, did you store data?")
    print("DATABASE: nJoyPorn database loaded")
    fullList = metaInformationObjectList.copy()
    file.close()

def LoadPornhubDB():
    pornhubScraper.InitDB()
    GetPornHubDataBase()
    global metaInformationObjectList
    global pornhubMetaInformationObjectList
    tempList = metaInformationObjectList.copy()
    for metaInformationObject in pornhubMetaInformationObjectList:
        tempList.append(metaInformationObject)
    global fullList
    fullList = tempList.copy()
    
def LoadFapsterDB():
    fapsterScraper.InitDB()
    GetFapsterDatabase()
    global fullList
    for metaInformationObject in fapsterMetaInformationObjectList:
        fullList.append(metaInformationObject)
    
def LoadHotExPornToonsDB():
    hotexporntoonsScraper.InitDB()
    GetHotExPornToonsDatabase()
    global fullList
    for metaInformationObject in hotexporntoonsMetaInformationObjectList:
        fullList.append(metaInformationObject)

def LoadTagList(_line):
    tagList = []
    result = re.findall(tagListPatter, _line)
    for tag in result:
        tagList.append(tag)
    return tagList

def LoadUserPageCategorieList():
    file = open(os.getcwd()+"/data/dictionarys/userPageCategorieDictionary")
    lines = file.readlines()
    file.close()
    global userPageCategorieList
    for line in lines:
        userPageCategorieList.append(line)
    print("DATABASE: userPageCategorieList loaded")

def ReloadDB():
    InitDatabase()
    #LoadDB()
                    
def Run():
    command = input("Enter command: [--initdb, --add, --addall, --edit, --printdb, --remove, --help]")
    if command == "--initdb":
        InitDatabase()
        Run()
    if command == "--add":
        print(end="", flush=True)
        LoadMetaInformationObjectList()
        AddVideo()
    if command == "--addall":
        AddAllLocalVideosToDatbase()
    if command == "--edit":
        print(end="", flush=True)
        LoadMetaInformationObjectList()
        EditVideo()
    if command == "--printdb":
        print(end="", flush=True)
        PrintDataBaseContent()
    if command == "--remove":
        print(end="", flush=True)
        command = input("Remove data by --fileName or --id: ")
        if command == "--id":
            RemoveVideoFromDatabaseById()
        if command == "--fileName":
            RemoveVideoFromDatabase()
    if command == "--updateModule":
        ModuleUpdate()
    if command == "--exit":
        exit()
    if command == "--help":
        print(end="", flush=True)
        print("This is the help page for gilltrickdb:\n You can enter these commands:\n --initdb: this initializes the database its like reloading\n --help: Prints this page")
        input("Press Enter to exit help")
        Run()

def RemoveVideoFromDatabase():
    fileName = input("Enter file name (with extension): ")
    global metaInformationObjectList
    if len(metaInformationObjectList) < 1:
        InitDatabase()
    path = "/static/storage/specials/"
    for metaInformationObject in metaInformationObjectList:
        fName = re.sub(path, "", metaInformationObject.videoUrl)
        if fName == fileName:
            command = input("Do you want to remove the file: " + fileName + "? ")
            if command == "y" or command == "-y" or command == "--y" or command == "yes" or command == "-yes" or command == "--yes":
                path = metaInformationObject.videoUrl
                metaInformationObjectList.remove(metaInformationObject)
                print("File: " +fileName + " removed from database")
                command = input("Do you want to delete the file permanently? ")
                if command == "y" or command == "-y" or command == "--y" or command == "yes" or command == "-yes" or command == "--yes":
                    os.remove(os.getcwd()+path)
                    thumbnailFolderPath = os.getcwd() + re.sub("/specials/", "/specials/thumbnails/", path)
                    DeleteThumbNails(thumbnailFolderPath)
                    print("File " + fileName + " got deleted!")
            SaveMetaInformationObjectList()

def RemoveVideoFromDatabaseById():
    fileName = input("Enter vidoe-id: ")
    global metaInformationObjectList
    if len(metaInformationObjectList) < 1:
        InitDatabase()
    for metaInformationObject in metaInformationObjectList:
        if metaInformationObject.id == fileName:
            command = input("Do you want to remove the file: " + fileName + " from database? ")
            if command == "y" or command == "-y" or command == "--y" or command == "yes" or command == "-yes" or command == "--yes":
                metaInformationObjectList.remove(metaInformationObject)
                print("File: " +fileName + " removed from database")
            SaveMetaInformationObjectList()
                 
def LoadMetaInformationObjectList():
    if os.path.exists(os.getcwd()+"/data/databases/videoDatabase.db"):
        file = open(os.getcwd()+"/data/databases/videoDatabase.db", "rb")
        global metaInformationObjectList
        metaInformationObjectList = pickle.load(file)
        file.close()
        return metaInformationObjectList
    command = input("No database file found.\nCreate a new file? ")
    if command == "y" or command == "-y" or command == "--y" or command == "yes" or command == "-yes" or command == "--yes":
        file = open(os.getcwd()+"/data/databases/videoDatabase.db", "wb")
        file.close()

def SaveMetaInformationObjectList():
    file = open(os.getcwd()+"/data/databases/videoDatabase.db", "wb")
    global metaInformationObjectList
    pickle.dump(metaInformationObjectList, file)
    file.close()
    
def AddVideo():
    global metaInformationObjectList
    print("Enter video data:")
    fileName = input("Enter filen name (with extension): ")
    videoUrl = videoStoragePath + fileName
    for metaInformationObject in metaInformationObjectList:
        if metaInformationObject.videoUrl == videoUrl:
            print("Cant't add the same file name a second time to database")
            AddVideo()
    videoTitle = input("Enter video name: ")
    videoDuration = GetVideoDuration(os.getcwd()+"/"+videoUrl)
    rating = input("Enter video rating: ")
    tagList = re.split("\s+", input("Enter tags: "))
    command = input("Create thumbnails?\nOr enter new path: ")
    if command == "y" or command == "-y" or command == "--y" or command == "yes" or command == "-yes" or command == "--yes":
        CreateThumbnails(fileName)
        folderName = re.sub(".mp4", "", fileName)
        thumbnailPath = "/static/storage/specials/thumbnails/" + folderName + "/0.png"
        command = ""
    if command != "":
        thumbnailPath = command
    discription = input("Enter video discription: ")
    id = input("Leaf blank for random id or \nAdd id: ")
    if id == "":
        id = CreateRandomId()
    origin = input("Enter origin (leaf blank for njoyporn): ")
    if origin == "":
        origin = "njoyporn"
    price = int(input("Enter price (in USD): "))
    if price == "":
        price == 0
    metaInformationObject = modules.MetaInformationObject()
    metaInformationObject.videoUrl = videoUrl
    metaInformationObject.videoTitle = videoTitle
    metaInformationObject.videoDuration = videoDuration
    metaInformationObject.rating = rating
    metaInformationObject.tagList = tagList
    metaInformationObject.thumbnailPath = thumbnailPath
    metaInformationObject.discription = discription
    metaInformationObject.id = id
    metaInformationObject.origin = origin
    metaInformationObject.price = price
    metaInformationObject.currency = "USD"
    command = input("Write video data to database? (y/n)")
    if command == "y" or command == "-y" or command == "--y" or command == "yes" or command == "-yes" or command == "--yes":  
        metaInformationObjectList.append(metaInformationObject)
        SaveMetaInformationObjectList()
    return None

def EditVideo():
    fileName = videoStoragePath + input("Enter file name (with extension): ")
    if fileName == videoStoragePath + "--exit":
            exit()
    if fileName == videoStoragePath + "--return":
        Run()
        return
    if fileName == videoStoragePath + "--id":
        EditById()
        return
    global metaInformationObjectList
    tagString = ""
    tagList = []
    for metaInformationObject in metaInformationObjectList:
        
        if metaInformationObject.videoUrl == fileName:
            videoUrl = fileName
            videoTitle = input("Enter video name: ")           
            print("New VideoTitle: " + videoTitle)
            if videoTitle == "":
                print("No change on video title")
                videoTitle = metaInformationObject.videoTitle
            videoDuration = GetVideoDuration(os.getcwd()+"/"+fileName)
            
            rating = input("Enter video rating: ")
            if rating == "":
                rating = metaInformationObject.rating
                
            for tag in metaInformationObject.tagList:
                tagString += "," + tag
                
            print("Current tags: " + tagString)
            command = input("Enter commad for editing the tag list (--replace, --remove, --add)")
            
            if command == "":
                tagList = metaInformationObject.tagList
            
            if command == "--replace":
                replaceWhat = input("Replace: ")
                replaceWith = input("with: ")
                for tag in metaInformationObject.tagList:
                    if tag == replaceWhat:
                        metaInformationObject.tagList.remove(tag)
                        metaInformationObject.tagList.append(replaceWith)
                        tagList = metaInformationObject.tagList
                        
            if command == "--remove":
                removeWhat = input("Remove: ")
                for tag in metaInformationObject.tagList:
                    if tag == removeWhat:
                        metaInformationObject.tagList.remove(tag)
                        
            if command == "--add":     
                tempTagList = re.split("\s+", input("Enter tag(s): "))
                tagList = metaInformationObject.tagList
                for tag in tempTagList:
                    tagList.append(tag)
            
            if command == "--duration":
                videoDuration = input("Enter video duration in seconds: ")
            
            discription = input("Change discrioption: ")
            if discription == "":
                discription = metaInformationObject.discription
                
            id = input("Enter id (--rnd) for a new random id")
            if id == "--rnd":
                id = CreateRandomId()
            if id == "":
                id = metaInformationObject.id
            
            origin = input("Enter origin: ")
            if origin == "":
                origin = metaInformationObject.origin
            
            thumbnailPath = input("Leaf blank to stay untouched, enter -create to create thumbnails or\nEnter new thumbnail image file: ")
            if thumbnailPath == "-create":
                fileName = re.sub(videoStoragePath, "", fileName)
                CreateThumbnails(fileName)
                folderName = re.sub(".mp4", "", fileName)
                thumbnailPath = "/static/storage/specials/thumbnails/" + folderName + "/0.png"                
            if thumbnailPath == "":
                thumbnailPath = metaInformationObject.thumbnailPath    
            owner = input("Change owner id: ")
            if owner == "":
                owner = metaInformationObject.owner
            price = input("Enter new price: ")
            if price == "":
                price = 0
            command = input("Enter new Trailer-Id for a new id or enter -clear for remove entry\nLeaf blank for no change: ")
            if command == "-clear":
                metaInformationObject.trailerId = ""
                command = ""
            if command != "":
                metaInformationObject.trailerId = command
            command = input("Enter new SellVideo-Id for a new id or enter -clear for remove entry\nLeaf blank for no change: ")
            if command == "-clear":
                metaInformationObject.sellVideoId = ""
                command = ""
            fileName = input("Edit filename: ")
            if command != "":
                metaInformationObject.sellVideoId = command        
            command = input("Edit comments? ")
            if command == "y" or command == "-y" or command == "--y" or command == "yes" or command == "-yes" or command == "--yes":
                RemoveCommentFromList(metaInformationObject.id)   
            metaInformationObject.videoUrl = videoUrl
            metaInformationObject.videoTitle = videoTitle
            metaInformationObject.videoDuration = videoDuration
            metaInformationObject.rating = rating
            metaInformationObject.tagList = tagList
            metaInformationObject.discription = discription
            metaInformationObject.id = id
            metaInformationObject.origin = origin
            metaInformationObject.thumbnailPath = thumbnailPath
            metaInformationObject.owner = owner
            metaInformationObject.price = int(price)
            metaInformationObject.fileName = fileName
            command = input("Write video data to database? (y/n)")
            if command == "y" or command == "-y" or command == "--y" or command == "yes" or command == "-yes" or command == "--yes":  
                SaveMetaInformationObjectList()
                print("Enter --return / --exit for fila-name to return to main menu or exit database")
                EditVideo()

def EditById():
    id = input("Enter id: ")
    global metaInformationObjectList
    tagString = ""
    tagList = []
    for metaInformationObject in metaInformationObjectList:
        
        if metaInformationObject.id == id:
            videoUrl = input("Enter video url: ")
            if videoUrl == "":
                videoUrl = metaInformationObject.videoUrl
            videoTitle = input("Enter video name: ")           
            print("New VideoTitle: " + videoTitle)
            if videoTitle == "":
                print("No change on video title")
                videoTitle = metaInformationObject.videoTitle
            videoDuration = GetVideoDuration(os.getcwd()+"/"+videoUrl)
            
            rating = input("Enter video rating: ")
            if rating == "":
                rating = metaInformationObject.rating
                
            for tag in metaInformationObject.tagList:
                tagString += "," + tag
                
            print("Current tags: " + tagString)
            command = input("Enter commad for editing the tag list (--replace, --remove, --add)")
            
            if command == "":
                tagList = metaInformationObject.tagList
            
            if command == "--replace":
                replaceWhat = input("Replace: ")
                replaceWith = input("with: ")
                for tag in metaInformationObject.tagList:
                    if tag == replaceWhat:
                        metaInformationObject.tagList.remove(tag)
                        metaInformationObject.tagList.append(replaceWith)
                        tagList = metaInformationObject.tagList
                        
            if command == "--remove":
                removeWhat = input("Remove: ")
                for tag in metaInformationObject.tagList:
                    if tag == removeWhat:
                        metaInformationObject.tagList.remove(tag)
                        
            if command == "--add":     
                tempTagList = re.split("\s+", input("Enter tag(s): "))
                tagList = metaInformationObject.tagList
                for tag in tempTagList:
                    tagList.append(tag)
            
            if command == "--duration":
                videoDuration = input("Enter video duration in seconds: ")
            
            discription = input("Change discrioption: ")
            if discription == "":
                discription = metaInformationObject.discription
                
            id = input("Enter id (--rnd) for a new random id")
            if id == "--rnd":
                id = CreateRandomId()
            if id == "":
                id = metaInformationObject.id
            
            origin = input("Enter origin: ")
            if origin == "":
                origin = metaInformationObject.origin
            
            thumbnailPath = input("Leaf blank to stay untouched, enter -create to create thumbnails or\nEnter new thumbnail image file: ")
            if thumbnailPath == "-create":
                fileName = re.sub(videoStoragePath, "", videoUrl)
                CreateThumbnails(videoUrl)
                folderName = re.sub(".mp4", "", fileName)
                thumbnailPath = "/static/storage/specials/thumbnails/" + folderName + "/0.png"                
            if thumbnailPath == "":
                thumbnailPath = metaInformationObject.thumbnailPath    
            owner = input("Change owner id: ")
            if owner == "":
                owner = metaInformationObject.owner
            price = input("Enter new price: ")
            if price == "":
                price = 0
            command = input("Enter new Trailer-Id for a new id or enter -clear for remove entry\nLeaf blank for no change: ")
            if command == "-clear":
                metaInformationObject.trailerId = ""
                command = ""
            if command != "":
                metaInformationObject.trailerId = command
            command = input("Enter new SellVideo-Id for a new id or enter -clear for remove entry\nLeaf blank for no change: ")
            if command == "-clear":
                metaInformationObject.sellVideoId = ""
                command = ""
            #fileName = input("Edit filename: ")
            if command != "":
                metaInformationObject.sellVideoId = command        
            command = input("Edit comments? ")
            if command == "y" or command == "-y" or command == "--y" or command == "yes" or command == "-yes" or command == "--yes":
                RemoveCommentFromList(metaInformationObject.id)   
            metaInformationObject.videoUrl = videoUrl
            metaInformationObject.videoTitle = videoTitle
            metaInformationObject.videoDuration = videoDuration
            metaInformationObject.rating = rating
            metaInformationObject.tagList = tagList
            metaInformationObject.discription = discription
            metaInformationObject.id = id
            metaInformationObject.origin = origin
            metaInformationObject.thumbnailPath = thumbnailPath
            metaInformationObject.owner = owner
            metaInformationObject.price = int(price)
            #metaInformationObject.fileName = fileName
            command = input("Write video data to database? (y/n)")
            if command == "y" or command == "-y" or command == "--y" or command == "yes" or command == "-yes" or command == "--yes":  
                SaveMetaInformationObjectList()
                print("Enter --return / --exit for fila-name to return to main menu or exit database")
                EditVideo()

def AddAllLocalVideosToDatbase():
    command = input("Whipe list? ")
    if command == "y" or command == "-y" or command == "--y" or command == "yes" or command == "-yes" or command == "--yes": 
        os.remove(os.getcwd()+"/data/databases/videoDatabase.db")
        file = open(os.getcwd()+"/data/databases/videoDatabase.db", "wb")
        file.close()
    print("This function will set up a minimal dataset to run the application.\nYou are not able to enter specific data!")
    RenameFiles()
    RemoveUmlautFromString()
    InitDatabase()
    baseUrl = "/static/storage/specials/"
    nameList = os.listdir(os.getcwd()+baseUrl)
    nameList.remove("thumbnails")
    for name in nameList:
        videoTitle = re.sub("\d* - ", "", re.sub(baseUrl, "", re.sub(".mp4", "", name)))
        thumbnailPath = baseUrl +  "thumbnails/"+re.sub(".mp4", "", name)+"/1.png"
        videoUrl = baseUrl + name
        tag = re.search("(\d*)", name).group(1)
        if MetaInformationObejctDuplication(videoUrl) == False:
            metaInformationObject = modules.MetaInformationObject()
            metaInformationObject.videoUrl = videoUrl 
            metaInformationObject.videoTitle = videoTitle
            metaInformationObject.tagList.append(tag)
            metaInformationObject.videoDuration = str(SecondsToTimeString(GetVideoDuration(os.getcwd()+"/"+videoUrl)))
            metaInformationObject.viewCount = 0
            metaInformationObject.origin = "dragonball"
            metaInformationObject.id = CreateRandomId()
            CreateThumbnails(name)
            metaInformationObject.thumbnailPath = thumbnailPath
            metaInformationObjectList.append(metaInformationObject)
        SaveMetaInformationObjectList()

def CreateDummyObject():
    print("DATABASE: Creating dummy object check you database")
    dummy = modules.MetaInformationObject()
    dummy.videoTitle = "This is a dommy object"
    dummy.videoDuration = "123"
    dummy.videoUrl = "/static/data/__/ahahah_low.mp4"
    dummy.thumbnailPath = "/static/data/__/thumbnails/ahahah_low/0.png"
    dummy.rating = 5
    dummy.origin = "free"
    dummy.discription = "This dummy object goets created for demonstration porpuses"
    return dummy
        
def SearchByKeyword(_keyWords):
    global fullList
    resultList = []
    if len(fullList) < 1:
        resultList.append(CreateDummyObject())
        return resultList
    tempList = fullList.copy()
    ungready = False
    if _keyWords[0] == "":
        #resultList = tempList
        return RandomResultList()
    if _keyWords[0] == "-ug":
        _keyWords.remove(_keyWords[0])
        ungready = True
    if _keyWords[0] == "--ph":
        return pornhubMetaInformationObjectList
    if _keyWords[0] == "-selected":
        if len(_keyWords) == 1:
            global metaInformationObjectList
            njoyPornList = metaInformationObjectList.copy()
            njoyPornList = ExcludeForSaleObjects(njoyPornList)
            return njoyPornList
        if _keyWords[1] != "":
            _keyWords.remove(_keyWords[0])
            tempList = metaInformationObjectList.copy()
    gotcha = False
    tempList = ExcludeForSaleObjects(tempList)
    if ungready == False:
        for keyWord in _keyWords:
            for metaInformationObject in tempList:
                if keyWord in metaInformationObject.videoTitle and gotcha == False:
                    gotcha = True
                    resultList.append(metaInformationObject)
                    tempList.remove(metaInformationObject)
                if gotcha == False:
                    for tag in metaInformationObject.tagList:
                        if tag == keyWord:
                            gotcha = True
                            resultList.append(metaInformationObject)
                            tempList.remove(metaInformationObject)
                            break
                gotcha = False
    if ungready == True:
        greadyMatch = False
        for metaInformationObject in tempList:
            for keyWord in _keyWords:
                if keyWord not in fullList.tagList:
                    break
                if keyWord in fullList.tagList:
                    greadyMatch = True
            if greadyMatch == True:
                resultList.append(metaInformationObject)
                tempList.remove(metaInformationObject)
                greadyMatch = False
    print("DEBUG: resultList.length:  " + str(len(resultList)))
    return resultList

def ExcludeForSaleObjects(_list):
    resultList = []
    for object in _list:
        if object.videoType != "forSale" and object.videoType != "private":
            resultList.append(object)
    return resultList

def ExcludeTrailerObjects(_list):
    resultList = []
    for object in _list:
        if object.videoType != "trailer":
            resultList.append(object)
    return resultList

def RandomResultList():
    global fullList
    global metaInformationObjectList
    if len(fullList) < 32:
        return fullList
    tempList = fullList.copy()
    tempList = ExcludeForSaleObjects(tempList)
    resultList = []
    for i in range(32):
        randomNumber = random.randint(0, (len(tempList)-1))
        if i % 5:
            resultList.append(tempList[randomNumber])
        else:
            resultList.append(metaInformationObjectList[random.randint(0, (len(metaInformationObjectList)-1))])
        tempList.remove(tempList[randomNumber])
        print("DEBUG: len(resultList) >> " + str(len(tempList)))
    return resultList   

def GetMetaInfromationObjectByVideoUrl(_videoUrl):
    global fullList
    for metaInformationObject in fullList:
        if metaInformationObject.videoUrl == _videoUrl:
            return metaInformationObject
    return "invalid"

def GetMetaInformationObjectById(_id):
    global fullList
    for metaInformationObject in fullList:
        if metaInformationObject.id == _id:
            return metaInformationObject
    return "invalid"

def PrintDataBaseContent():
    if os.path.exists(os.getcwd()+"/data/databases/videoDatabase.db"):
        file = open(os.getcwd()+"/data/databases/videoDatabase.db", "rb")
        global metaInformationObjectList
        metaInformationObjectList = pickle.load(file)
        file.close()
        tagListLine = ""
        for metaInformationObject in metaInformationObjectList:
            for tag in metaInformationObject.tagList:
                tagListLine += " "+ tag
            print("Video Title: " + metaInformationObject.videoTitle + "\nVideoPath: " + metaInformationObject.videoUrl + "\nVideo Rating: " + str(metaInformationObject.rating) + "\nVideoDuration: " + str(metaInformationObject.videoDuration) + "\nTag-List: " + tagListLine + "\nThumbnail-Path: " + metaInformationObject.thumbnailPath + "\nDiscription: " + metaInformationObject.discription + "\nID: " + metaInformationObject.id + "\nOrigin: " + metaInformationObject.origin + "\nOwner: " + metaInformationObject.owner + "\nView-Count: "+ str(metaInformationObject.viewCount) + "\nView-Count: "+ str(metaInformationObject.price), metaInformationObject.currency + "\nVideo-Type: "+ metaInformationObject.videoType + "\nTrailer-Id: "+ metaInformationObject.trailerId + "\nFile-Name: "+ metaInformationObject.fileName + "\nSaleVideo-Id: "+ metaInformationObject.sellVideoId + "\nPrice: "+ str(metaInformationObject.price) + "\n")
            tagListLine = ""
        print("Record Count: ", len(metaInformationObjectList))
        Run()
        return
    print("No database file found")

def UpdateMetaInformationObject(_id, _varibleName, _value):
    global fullList
    for metaInformationObject in fullList:
        if metaInformationObject.id == _id:
            if _varibleName == "upVote":
                metaInformationObject.upVotes += str(_value)
            if _varibleName == "downVote":
                metaInformationObject.downVotes += _value
            if _varibleName == "viewCount":
                metaInformationObject.viewCount += 1
            if _varibleName == "commentList":
                metaInformationObject.commentObjectList.append(_value)
            print("DATBASE: metaInformationObject with id: " + _id + " updated")

def CreateRandomId():
    return hashlib.md5(str(datetime.datetime.now()).encode()).hexdigest()

def LoadCategorieList():
    global categoryNameList
    categoryListFile = open(os.getcwd()+"/data/dictionarys/categorieDictionary", "r")
    categoryNameList = categoryListFile.readlines()
    LoadPopularCategoryList()

def LoadPopularCategoryList():
    global categoryNameList
    global popularCategoriesList
    popularCategoriesList.clear()
    tempList = categoryNameList.copy()
    for i in range(18):
        randomNumber = random.randint(0, len(tempList)-1)
        popularCategoriesList.append(tempList[randomNumber])
        tempList.remove(tempList[randomNumber])
        
def LoadPornStarNameList():
    global pornStarNameList
    global popularPornStarList
    categoryListFile = open(os.getcwd()+"/data/dictionarys/pornStarNameDictionary", "r")
    pornStarNameList = categoryListFile.readlines()
    LoadPopularPornStarList()

def LoadPopularPornStarList():
    global pornStarNameList
    global popularPornStarList
    payedPornStarList = ["Delphoxi", "Crystal Cherrie", "Ksew Meow"]
    popularPornStarList.clear()
    for payedPornStar in payedPornStarList:
        popularPornStarList.append(payedPornStar)
    tempList = pornStarNameList.copy()
    for i in range(18-len(payedPornStarList)):
        randomNumber = random.randint(0, len(tempList)-1)
        popularPornStarList.append(tempList[randomNumber])
        tempList.remove(tempList[randomNumber])
    shuffleList =  ShuffleList(popularPornStarList)
    popularPornStarList = shuffleList
        
def ShuffleList(_list):
    tempList = _list.copy()
    _list.clear()
    for entry in range(len(tempList)):
        randomNumber = random.randint(0, len(tempList)-1)
        _list.append(tempList[randomNumber])
        tempList.remove(tempList[randomNumber])
    return _list
                               
def GetMetaInformationObjectList():
    global metaInformationObjectList
    return metaInformationObjectList

def GetPornHubDataBase():
    global pornhubMetaInformationObjectList
    pornhubMetaInformationObjectList = pornhubScraper.GetPornhubDatabase()

def GetFapsterDatabase():
    global fapsterMetaInformationObjectList
    fapsterMetaInformationObjectList = fapsterScraper.GetFapsterDatabase()

def GetHotExPornToonsDatabase():
    global hotexporntoonsMetaInformationObjectList
    hotexporntoonsMetaInformationObjectList = hotexporntoonsScraper.GetExPornToonsDatabase()

def UpdatePopularCategoriesList():
    global popularCategoriesList
    popularCategoriesList = analytics.LoadPopularCategorieList()

def GetPopularCategoriesList():
    global popularCategoriesList
    return popularCategoriesList

def UpdatePopularPornStarList():
    global popularPornStarList
    popularPornStarList = analytics.LoadPopularPornStarList()

def GetPopularPornStarList():
    global popularPornStarList
    return popularPornStarList
   
def GetHtml(_url):
    header = Headers(browser="chrome", os="win", headers=True) 
    return requests.get(_url, headers=header.generate()).text

def CreateThumbnails(_videoFileName):
    print("Extract frames from video")
    folderName = re.sub(".mp4", "", _videoFileName)
    try:
        os.mkdir(os.getcwd()+"/static/storage/specials/thumbnails/"+folderName)
    except:
        print("DATABASE: Can't create thumbnails, folder allready exists")
        return
    frames = GetFramesFromVideo(os.getcwd()+"/static/storage/specials/"+_videoFileName)
    print("Generate and save thumbs for: " + _videoFileName)
    for i in range(len(frames)):
        thumb = ConverImageToThumNail(frames[i])
        for k, v in thumb.items():
            cv2.imwrite(os.getcwd()+"/static/storage/specials/thumbnails/" + folderName + "/" + str(i) + ".png", v)

def DeleteThumbNails(_thumbanailFolderPath):
    _thumbanailFolderPath = re.sub(".mp4", "", _thumbanailFolderPath)
    thumbnails = os.listdir(_thumbanailFolderPath)
    for thumbnail in thumbnails:
        os.remove(_thumbanailFolderPath+"/"+thumbnail)
    os.rmdir(_thumbanailFolderPath)
    print("DATABASE: Thumbnails in " + _thumbanailFolderPath + " delteted")
         
def GetFramesFromVideo(video_filename):
    cap = cv2.VideoCapture(video_filename)
    videoLength = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) - 1
    frames = []
    if cap.isOpened() and videoLength > 0:
        frame_ids = [0]
        if videoLength >= 4:
            frame_ids = [0.01,
                         round(videoLength * 0.25),
                         round(videoLength * 0.5),
                         round(videoLength * 0.75),
                         videoLength - 1]
        count = 0
        success, image = cap.read()
        while success:
            if count in frame_ids:
                frames.append(image)
            success, image = cap.read()
            count += 1
    return frames

def ConverImageToThumNail(img):
    height, width, channels = img.shape
    thumbs = {"original": img}
    reolutionLIst = [1080, 720, 640, 320, 160]
    for resolution in reolutionLIst:
        if (width >= resolution):
            r = (resolution + 0.0) / width
            maxSize = (resolution, int(height * r))
            thumbs[str(resolution)] = cv2.resize(img, maxSize, interpolation=cv2.INTER_AREA)
    return thumbs

def SecondsToTimeString(_seconds):
    hours = 0
    minutes = 0
    seconds = _seconds
    while seconds > 59:
        seconds -= 60
        minutes += 1
    while minutes > 60:
        minutes -= 60
        hours +=1
    if hours < 10:
        strh = "0" + str(hours)
    if hours >= 10:
        strh = str(hours)
    if minutes < 10:
        strm = "0" + str(minutes)
    if minutes >= 10:
        strm = str(minutes)
    if seconds < 10:
        strs = "0" + str(seconds)
    if seconds >= 10:
        strs = str(seconds)
    timeString = strh + ":" + strm + ":" + strs
    return timeString

def AddComment(_videoId, _commentContent, _writerName):
    metaInformationObject = GetMetaInformationObjectById(_videoId)
    comment = modules.CommentObject()
    comment.createdOn = datetime.datetime.now().strftime("%B %d, %Y") + " @ " + datetime.datetime.now().strftime("%H:%M:%S")
    comment.id = CreateRandomId()
    comment.metaInformatinoObjectId = _videoId
    comment.text = _commentContent
    comment.writerNickName = _writerName
    metaInformationObject.commentObjectList.append(comment)
    SaveMetaInformationObjectList()

def MetaInformationObejctDuplication(_vidoeUrl):
    global metaInformationObjectList
    for metaInformationobject in metaInformationObjectList:
        if _vidoeUrl == metaInformationobject.videoUrl:
            print("Duplication for: " + _vidoeUrl + " dumping data")
            return True
    return False

def RemoveUmlautFromString(_string):
    print("STRING: " + _string)
    if "Ü" in _string:
        _string = re.sub("Ü", "Ue", _string)
    if "ü" in _string:
        _string = re.sub("ü", "ue", _string)
    if "Ä" in _string:
        _string = re.sub("Ä", "Ae", _string)
    if "ä" in _string:
        _string = re.sub("ä", "ae", _string)
    if "Ö" in _string:
        _string = re.sub("Ö", "Oe", _string)
    if "ö" in _string:
        _string = re.sub("ö", "oe", _string)
    if "ß" in _string:
        _string = re.sub("ß", "ss", _string)
    print("STRING_N: " + _string)
    return _string 

def RenameFiles():
    folderPath = os.getcwd()+"/static/storage/specials/"
    fileList = os.listdir(folderPath)
    filePathList = []
    for file in fileList:
        filePathList.append(folderPath+file)
    for filePath in filePathList:
        Path(filePath).rename(RemoveUmlautFromString(filePath))

def GetTotalRecordsCount():
    global fullList
    return str(len(fullList * 100) + random.randint(0, 1000))  

def GetFileName(_file):
    result = re.search(fileNamePattern, _file)
    fileName = result.group(1)
    return fileName

def GetMetaInformationObjectByVideoTitle(_videoTitle):
    global metaInformationObjectList
    for metaInformationObject in metaInformationObjectList:
        if metaInformationObject.videoTitle == _videoTitle:
            return metaInformationObject
    return "invalid"

def GetUserVideoList(_userId):
    global metaInformationObjectList
    userVideoList = []
    for metaInformationObject in metaInformationObjectList:
        if metaInformationObject.owner == _userId:
            userVideoList.append(metaInformationObject)
    return userVideoList

#this function is modified for testing
# def GetUserVideoList(_userId):
#     print("!!!ATTENTION!!! Change this function back. if you se this on live server you are in trouble")
#     global metaInformationObjectList
#     userVideoList = []
#     userObject = userDatabase.LoadUserObjectById(_userId)
#     for videoId in userObject.videoList:
#         userVideoList.append(GetMetaInformationObjectById(videoId))
#     return userVideoList

def GetUserFavoriteList(_userId):
    global metaInformationObjectList
    favList = []
    userObject = userDatabase.LoadUserObjectById(_userId)
    for videoId in userObject.favoriteList:
        for metaInformationObject in metaInformationObjectList:
            if metaInformationObject.id == videoId:
                favList.append(metaInformationObject)
    return favList

def GetUserPurchasedVideosList(_userId):
    global metaInformationObjectList
    purchasedVideosList = []
    userObject = userDatabase.LoadUserObjectById(_userId)
    for videoId in userObject.purchasedVideosList:
        for metaInformationObject in metaInformationObjectList:
            if metaInformationObject.id == videoId:
                purchasedVideosList.append(metaInformationObject)
    return purchasedVideosList

def AddForSaleIdToMetaInformationObject(_trailerId, _videoId, _price):
    print("DEBUG DEBUG: AddForSaleIdToMetaInformationObject >>", _trailerId, _videoId)
    global metaInformationObjectList
    for metaInformationObject in metaInformationObjectList:
        if metaInformationObject.id == _trailerId:
            metaInformationObject.sellVideoId = _videoId
            metaInformationObject.price = _price
    SaveMetaInformationObjectList()
    return None

################################## H E L P E R ####################################
#
####################### I use this function to copy data ##########################
# 
# def VideoUrlToThumbnailPath():
#     InitDatabase()
#     global metaInformationObjectList
#     for metaInformationObject in metaInformationObjectList:
#         result = re.search("\/static\/storage\/specials\/(.*)\.mp4", metaInformationObject.videoUrl)
#         thumbnailPath = "/static/storage/specials/thumbnails/" + result.group(1) +"/0.png"
#         print(thumbnailPath)
#         metaInformationObject.thumbnailPath = thumbnailPath
#     SaveMetaInformationObjectList()
#
###################################################################################
#
###################### I use this function i update a module ######################
#
############################ L O G I C - S E C T I O N ############################
#
# create the new module call it newModule
# create a backup copy of your data
#
# function call:
#
# load all of the current data
# create a temporary list for the new modules
# loop through the current list
# create a new object of the new module
# copy the current data to the new module
# REMEMBER: If you change the varible names you brake a lot of code
#           But its quit easy to fix by using some find and replace
# let the new varibles untouched
# add the newModule object to the newModuleList
# clear the current global metaInformationObjectList
# copy new module list to global metaInformationObjectList
# Call The SaveMetaInformationObjectList function to save the updates modules list
#
# add the new varibles to the outdates MetaInformationObject class
# restart database.py
# start database.py -> --initdb -> --printdb
#
# if there is the same data then before everything worked well
# functions to update in database.py:
#   --add
#   --edit
#   --print
#
###################################################################################
#   
def ModuleUpdate():
    print("Activate function first")
    # command = input("Did you make a backup and modified the function? ")
    # if command != "yes":
    #     return
    # InitDatabase()
    # global metaInformationObjectList
    # global pornhubMetaInformationObjectList
    # global fapsterMetaInformationObjectList
    # newModuleList = []
    # for metaInformationObject in metaInformationObjectList:
    #     newModule = modules.newModule()
    #     #newModule = modules.MetaInformationObject()
    #     newModule.videoUrl = metaInformationObject.videoUrl
    #     newModule.videoTitle = metaInformationObject.videoTitle
    #     newModule.videoDuration = metaInformationObject.videoDuration
    #     newModule.rating = metaInformationObject.rating
    #     newModule.tagList = metaInformationObject.tagList
    #     newModule.thumbnailPath = metaInformationObject.thumbnailPath
    #     newModule.discription = metaInformationObject.discription
    #     newModule.id = metaInformationObject.id
    #     newModule.data = metaInformationObject.data
    #     newModule.upVotes = 0
    #     newModule.downVotes = 0
    #     newModule.categoryList = metaInformationObject.tagList
    #     newModule.origin = "njoyporn"
    #     newModule.owner = ""
    #     newModule.createdOn = ""
    #     newModule.sponsor = ""
    #     newModule.commentObjectList = []
    #     newModule.viewCount = 0
    #     newModule.price = 0
    #     newModule.currency = "USD"
    #     newModuleList.append(newModule)
    # metaInformationObjectList.clear()
    # metaInformationObjectList = newModuleList.copy()
    # print("Module updatet")
    # SaveMetaInformationObjectList()
    # return True
#
# i will use this function to add random ids to all the old data
#
# def Temp():
#     InitDatabase()
#     global metaInformationObjectList
#     for metaInformationObject in metaInformationObjectList:
#         metaInformationObject.id = CreateRandomId()
#     SaveMetaInformationObjectList()
#
# run the ModuleUpdate function again but replace newModule with MetaInformationObject
#
####################################################################################
#
### I use this function to create thubnails for every video in storage/specials ####
# 
######### Used this function to update the time of metainformationobjects ##########
#
# def ValueUpdate():
#     import time
#     InitDatabase()
#     global metaInformationObjectList
#     for metaInformationObject in metaInformationObjectList:
#         time.sleep(.7)
#         metaInformationObject.id = CreateRandomId()
#     SaveMetaInformationObjectList()
#
#####################################################################################

def CreateAllThumbnails():
    InitDatabase()
    global metaInformationObjectList
    # fileList = os.listdir(os.getcwd()+"/static/storage/specials/")
    # for file in fileList:
    #     CreateThumbnails(file)
    for metaInformationObject in metaInformationObjectList:
        videoUrl = metaInformationObject.videoUrl
        base = "/static/storage/specials/"
        videoUrl = re.sub(base, "", videoUrl)
        folderName = re.sub(".mp4", "", videoUrl)
        thumbnailPath = "/static/storage/specials/thumbnails/"+folderName+"/0.png"
        metaInformationObject.thumbnailPath = thumbnailPath
    SaveMetaInformationObjectList()
    
def RemoveCommentFromList(_videoId):
    command = input("Leaf blank to delete all or\nEnter comment-id: ")
    metaInformationObject = GetMetaInformationObjectById(_videoId)
    if command == "":
        metaInformationObject.commentObjectList.clear()
        print("All comments deleted")
    if command != "":
        for commentObject in metaInformationObject.commentObjectList:
            if commentObject.id == command:
                metaInformationObject.commentObjectList.remove(commentObject)
    commentCount = len(metaInformationObject.commentObjectList)
    print("Comment counter: " + str(len(metaInformationObject.commentObjectList)))
    if commentCount > 0:
        for comment in metaInformationObject.commentObjectList:
            print("Comment with id: " + comment.id + " left")
    
######################## W E B G U I - I M P L E M E N T A T I O N ########################
#
def From_GUI_EditVideo(_fileName, _videoTitle, _videoTags, _discription, _categories, _price):
    metaInformationObject = GetMetaInfromationObjectByVideoUrl("/static/storage/specials/"+_fileName)
    if metaInformationObject == "invalid":
        metaInformationObject = GetMetaInformationObjectById(_fileName)
        if metaInformationObject == "invalid":
            return metaInformationObject
    if _price != "" and metaInformationObject.videoType != "forSale":
        return "error you cant add a price to a item thats not setup for sale in the first place"
    metaInformationObject.videoTitle = _videoTitle
    metaInformationObject.tagList = re.split("\s", _videoTags)
    metaInformationObject.discription = _discription
    metaInformationObject.categoryList = re.split("\s", _categories)
    metaInformationObject.price = _price
    SaveMetaInformationObjectList()
    return "<script>alert(\"Your video got successfully updated.\");location.href = \"userAccount\";</script>"
    
def From_GUI_AddVideo(_fileName, _videoTitle, _videoTags, _discription, _categories, _username, _trailerId, _command, _price):  
    metaInformationObject = modules.MetaInformationObject()
    metaInformationObject.origin = "njoyporn"
    metaInformationObject.videoUrl = videoStoragePath + _fileName
    metaInformationObject.videoTitle = _videoTitle
    metaInformationObject.tagList = re.split("\s", _videoTags)
    metaInformationObject.videoDuration = SecondsToTimeString(GetVideoDuration(metaInformationObject.videoUrl))
    metaInformationObject.discription = _discription
    metaInformationObject.categoryList = re.split("\s", _categories)
    metaInformationObject.tagList = metaInformationObject.categoryList
    metaInformationObject.id = CreateRandomId()
    userObject = userDatabase.LoadUserObjectByName(_username)
    metaInformationObject.owner = userObject.id
    metaInformationObject.trailerId = _trailerId
    metaInformationObject.videoType = _command
    metaInformationObject.price = _price
    folderName = re.sub(".mp4", "", _fileName)
    thumbnailPath = "/static/storage/specials/thumbnails/" + folderName + "/0.png"
    metaInformationObject.thumbnailPath = thumbnailPath
    if _command != "forSale":
        CreateThumbnails(_fileName)
    if MetaInformationObejctDuplication(metaInformationObject.videoUrl) == False:
        global metaInformationObjectList
        if _trailerId != "" and _command == "forSale":
            AddForSaleIdToMetaInformationObject(_trailerId, metaInformationObject.id, metaInformationObject.price)
            trailerObject = GetMetaInformationObjectById(_trailerId)
            if userObject.role != "admin":
                if trailerObject.owner != userObject.id:
                    return render_template("error.html", error=modules.ErrorMessage("Forbidden","You dont own the trailer"))
            metaInformationObject.videoUrl = trailerObject.videoUrl
            metaInformationObject.thumbnailPath = trailerObject.thumbnailPath
            metaInformationObject.fileName = _fileName
            newFileName = re.sub("/static/storage/specials/", "", _fileName)
            Path(os.getcwd()+"/static/storage/specials/"+ _fileName).rename(os.getcwd()+"/protected/videos/"+newFileName)
        metaInformationObjectList.append(metaInformationObject)
        SaveMetaInformationObjectList()
        ReloadDB()
        userDatabase.UpdateUserVideoList(_username, metaInformationObject.id)
        communication.NotifyFollower(userObject, metaInformationObject)
        return "<script>alert(\"Your video got successfully added to the database.\");location.href = \"userAccount\";</script>"#war mal webgui
    return "<script>alert(\"Its seams your video is allready presistent in the database.\");location.href = \"userAccount\";</script>"  
    return "invalid"

def From_GUI_AddUserVideo(_fileName, _videoTitle, _videoTags, _discription, _categories, _username, _trailerId, _command, _price):
    print("Debug here")  
    metaInformationObject = modules.MetaInformationObject()
    metaInformationObject.origin = "njoyporn"
    metaInformationObject.videoUrl = videoStoragePath + _fileName
    metaInformationObject.videoTitle = _videoTitle
    metaInformationObject.tagList = re.split("\s", _videoTags)
    metaInformationObject.videoDuration = SecondsToTimeString(GetVideoDuration(metaInformationObject.videoUrl))
    metaInformationObject.discription = _discription
    metaInformationObject.categoryList = re.split("\s", _categories)
    metaInformationObject.id = CreateRandomId()
    userObject = userDatabase.GetUserByName(_username)
    metaInformationObject.owner = userObject.id
    metaInformationObject.trailerId = _trailerId
    metaInformationObject.videoType = _command
    metaInformationObject.price = _price
    folderName = re.sub(".mp4", "", _fileName)
    thumbnailPath = "/static/storage/specials/thumbnails/" + folderName + "/0.png"
    metaInformationObject.thumbnailPath = thumbnailPath
    if _command != "forSale":
        CreateThumbnails(_fileName)
    if MetaInformationObejctDuplication(metaInformationObject.videoUrl) == False:
        global metaInformationObjectList
        if _trailerId != "" and _command == "forSale":
            trailerObject = GetMetaInformationObjectById(_trailerId)
            if trailerObject.owner != userObject.id:
                return render_template("error.html", error=modules.ErrorMessage("Forbidden","You dont own the trailer"))
            print("DEBUG: _fileName >> " + _fileName)
            metaInformationObject.fileName = _fileName
            AddForSaleIdToMetaInformationObject(_trailerId, metaInformationObject.id, metaInformationObject.price)
            metaInformationObject.videoUrl = trailerObject.videoUrl
            metaInformationObject.thumbnailPath = trailerObject.thumbnailPath
            newFileName = re.sub("/static/storage/specials/", "", _fileName)
            Path(os.getcwd()+"/static/storage/specials/"+ _fileName).rename(os.getcwd()+"/protected/videos/"+newFileName)
        metaInformationObjectList.append(metaInformationObject)
        SaveMetaInformationObjectList()
        ReloadDB()
        userDatabase.UpdateUserVideoList(_username, metaInformationObject.id)
    return "<script>alert(\"Its seams your video is allready presistent in the database.\");location.href = \"userAccount\";</script>" 
    return "invalid"   

def From_GUI_RemoveVideo(_id):
    metaInformationObject = GetMetaInformationObjectById(_id)
    if metaInformationObject == "invalid":
        return render_template("error.htmt", error=modules.ErrorMessage("Video not Found in Database", "Check the id you enterd"))
    if QuickRemove(metaInformationObject):
        return "<script>alert(\"Your video got successfully removed from the database.\");location.href = \"webgui\";</script>"

def From_GUI_RemoveUserVideo(_videoId, _userId):
    userVideoList = GetUserVideoList(_userId)
    for userVideo in userVideoList:
        if userVideo.id == _videoId:
            QuickRemove(userVideo)
            return "<script>alert(\"Your video got successfully removed from the database.\");location.href = \"userAccount\";</script>" 
    return render_template("error.html", error=modules.ErrorMessage("Video not deleted", "Check the id or your password enterd")) 

def From_GUI_GetObjectsInUserCardList(_cardList):
    userCardListObjectList = []
    for id in _cardList:
        userCardListObjectList.append(GetMetaInformationObjectById(id))
    return userCardListObjectList
    
def QuickRemove(_metaInformationObject):
    global metaInformationObjectList
    path = "/static/storage/specials/"
    fName = re.sub(path, "", _metaInformationObject.videoUrl)
    path = _metaInformationObject.videoUrl
    metaInformationObjectList.remove(_metaInformationObject)
    try:
        print("File: " +fName + " removed from database")
        os.remove(os.getcwd()+path)
        print("File " + fName + " got deleted!")
        metaInformationObjectList.remove(_metaInformationObject)    
        SaveMetaInformationObjectList()
    except:
        print("File could not be deleted. Search for: " + fName)
        return True
    return True        
      
    
if __name__ == "__main__":
    Run()