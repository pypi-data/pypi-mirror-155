import requests, re, os, pickle, hashlib, datetime
from fake_headers import Headers
from nJoyPorn import modules

header = Headers(browser="chrome", os="win", headers=True)
metaInformationObjectList = []
currentScrapeList = []    
phPattern = "<div class=\"wrap\">\n?\s+?<div class=\"phimage\"\n?\s+?>\n?\s+?<div class=\"preloadLine\"><\/div>\n?\s+?<a href=\"(.*)\" title=\"(.*)\"\n?\s+?class=\"fade(.*)\n?\s+?data-related-url=\"(.*)\"\n?\s+?>\n?\s+?<img\n?\s+?src=\"(.*)\n?\s+?data-thumb_url\s?=\s?\"(.*)\"(\n|.)*?<var class=\"duration\">(.*)<\/var>\n?\s+?.*\n?\s+?.*\n?\s+?.*\n?\s+?.*\n?\s+?.*\n?\s+?.*\n?\s+?.*\n?\s+?.*\n?\s+?.*\n?\s+?.*\n?\s+?.*\n?\s+?.*\n?\s+?.*\n?\s+?.*\n?\s+?.*\n?\s+?.*\n?\s+?.*\n?\s+?.*\n?\s+?.*\n?\s+?.*\n?\s+?.*\n?\s+?.*\n?\s+?.*\n?\s+?.*\n\s+(.*)<"
phTagPattern = "<a class=\"item\" href=\"\/video\/search\?search=(\w+|\d+)?\+?(\w+|\d+)?\+?(\w+|\d+)?\+?(\w+|\d+)?"
ratingPattern = "(\d\d?)"

def CreateDictionary():
    keyWordDictionary = open(os.getcwd()+ "/data/dictionarys/keyWordDictionary" , "r")
    lines = keyWordDictionary.readlines()
    return lines

def Run():
    command = input("Enter command: [-initdb, -printdb, -search, -long, -help]")
    if command == "-initdb":
        InitDB()
        print("pornhubDatabase loaded with " + str(len(metaInformationObjectList)) + " records")
        Run()
    if command == "-printdb":
        LoadMetaInformationObjectList()
        PrintMetaInformationObjectList()
    if command == "-search":
        InitDB()
        EnterKeyWords()
    if command == "-long":
        InitDB()
        LongScrape()
    if command == "-exit":
        exit()
    if command == "-help":
        print("Learn how to deal with the issue... I dont care")
        Run()
    if command == "-updateModule":
        ModuleUpdate()
    print("Unknown Command...")
    Run()

def EnterKeyWords():
    keywords = re.split("\s+", input("Enter keywords for search: "))
    pageCount = int(input("How many pages to search: "))
    searchString = ""
    for word in keywords:
        if searchString != "": 
            searchString += "+"+word
        if searchString == "":
            searchString += word
    for page in range(pageCount):
        print("Extracting page: " + str(page))
        if page == 0:
            url = "https://de.pornhub.com/video/search?search="+searchString
        if page != 0:
            url = "https://de.pornhub.com/video/search?search="+searchString + "&page=" + str(page)
        ExtractDataFromSite(url)
    command = input("Save Data To DB? ")
    if command == "y":
        SaveMetaInformationObjectList()
    if command != "y":
        print("Dumping data")
    Run()
    
def ExtractDataFromSite(_url):
    global metaInformationObjectList
    if len(metaInformationObjectList) <1:
        LoadMetaInformationObjectList()   
    print("Try to grab page source code") 
    sourceCode = requests.get(_url, headers=header.generate()).text
    if sourceCode == "":
        print("Unable to grab the source code of the page...")
    print("Source code of page loaded")
    for match in re.finditer(phPattern, sourceCode):
        metaInformationObject = modules.MetaInformationObject()
        urlString = "https://www.pornhub.com"
        videoUrl = urlString + match.group(1)
        videoTitle = match.group(2)
        try:
            views = re.search("views\"><var>(.*)<\/var>", match.group(0)).group(1)
        except:
            views = "ka"
        try:
            owner = re.search("channels\/(.*)\"\s", match.group(0)).group(1)
        except:
            owner = "ka"
        try:
            rating = re.search("(\d\d?\d?)", match.group(9)).group(1)
        except:
            rating = "ka"
        videoDuration = match.group(8)
        thumbnailPath = match.group(6)
        if MetaInformationObejctDuplication(videoUrl) == False:
            metaInformationObject.videoUrl = videoUrl
            metaInformationObject.videoTitle = videoTitle
            metaInformationObject.viewCount = views
            metaInformationObject.rating = rating
            metaInformationObject.videoDuration = videoDuration
            metaInformationObject.thumbnailPath = thumbnailPath
            metaInformationObject.tagList = GrabTagList(videoUrl)
            metaInformationObject.id = CreateRandomId()
            metaInformationObject.origin = "pornhub"
            metaInformationObject.owner = owner
            if ValidMetaInformationObject(metaInformationObject) == True:
                metaInformationObjectList.append(metaInformationObject)
                
def MetaInformationObejctDuplication(_vidoeUrl):
    global metaInformationObjectList
    for metaInformationobject in metaInformationObjectList:
        if _vidoeUrl == metaInformationobject.videoUrl:
            print("Duplication for: " + _vidoeUrl + " dumping data")
            return True
    return False

def OK():
    return None

def GrabTagList(_url):
    sourceCode = requests.get(_url).text
    print("URL: " + _url + "\nVideo page source code loaded")
    tagList = []
    tag = ""
    for match in re.finditer(phTagPattern, sourceCode):
        for i in range(len(match.groups())):
            if tag != "":
                try:
                    tag += " " + match.group(i+1)
                except:
                    OK()
            if tag == "":
                try:
                    tag += match.group(i+1)
                except:
                    OK()
        tagList.append(tag)
        tag = ""
    tagList = list(dict.fromkeys(tagList))
    return tagList
    
def LongScrape():
    lineToStart = input("Enter the line you want to start with: ")
    if lineToStart == "":
        lineToStart = 0
    pageCount = 3
    keyWordList = CreateDictionary()
    skipedItemList = []
    for i in range(int(lineToStart)):
        skipedItemList.append(keyWordList[i])
        keyWordList.remove(keyWordList[i])
    for skipedItem in skipedItemList:
        print(skipedItem + " skiped")
    keyWordsLeft = len(keyWordList) - len(skipedItemList)
    print(str(keyWordsLeft) + " key words left to scrape")
    searchString = ""
    lineCounter = int(lineToStart)
    for keyWord in keyWordList:
        print("Key word: " + keyWord + "@ line " + str(lineCounter))
        searchString = re.sub("\s", "+", keyWord)
        for page in range(pageCount):
            print("Extracting page: " + str(page))
            if page == 0:
                url = "https://de.pornhub.com/video/search?search="+searchString
            if page != 0:
                url = "https://de.pornhub.com/video/search?search="+searchString + "&page=" + str(page)
            ExtractDataFromSite(url)
            SaveMetaInformationObjectList()
        lineCounter += 1
    Run()

def ValidMetaInformationObject(_metaInformationObject):
    if _metaInformationObject.videoUrl == "":
        print("no video url")
        return False
    if _metaInformationObject.videoTitle == "":
        print("no video title")
        return False
    if _metaInformationObject.videoDuration == "":
        print("no video duration")
        return False
    if len(_metaInformationObject.tagList) < 1:
        print("no tags")
        return False
    if _metaInformationObject.thumbnailPath == "":
        print("no thumbnail path")
        return False
    if _metaInformationObject.id == "":
        print("no id")
        return False
    return True

def InitDB():
    if os.path.exists(os.getcwd()+"/data/databases/pornhubdb.db"):
        LoadMetaInformationObjectList()
        return
    print("PORNHUB: No database file found")
    command = input("PORNHUB: Create a new file? ")
    if command == "yes":
        file = open(os.getcwd()+"/data/databases/pornhubdb.db", "wb")
        file.close()
        Run()

def SaveMetaInformationObjectList():
    global metaInformationObjectList
    file = open(os.getcwd()+"/data/databases/pornhubdb.db", "wb")
    pickle.dump(metaInformationObjectList, file)
    file.close()
    print("PORNHUB: Database saved")
    
def LoadMetaInformationObjectList():
    if os.path.exists(os.getcwd()+"/data/databases/pornhubdb.db"):
        global metaInformationObjectList
        file = open(os.getcwd()+"/data/databases/pornhubdb.db", "rb")
        try:
            metaInformationObjectList = pickle.load(file)
            print("PORNHUB: database loaded ")
        except:
            print("PORNHUB: No data in db or data is corrupted")
        file.close()
        return
    print("PORNHUB: Cant load database file")

def PrintMetaInformationObjectList():
    global metaInformationObjectList
    tagString = ""
    for metaInformationObject in metaInformationObjectList:
        for tag in metaInformationObject.tagList:
            if tagString != "":
                tagString += " " + tag
            if tagString == "":
                tagString += tag
        print("Video-Title: " + metaInformationObject.videoTitle + "\nRating: " + metaInformationObject.rating + "\nVideo-Url: " + metaInformationObject.videoUrl + "\nVideo-Duration: " + metaInformationObject.videoDuration + "\nVideo-Thumbnail: " + metaInformationObject.thumbnailPath + "\nTag-List: " + tagString + "\nID: " + metaInformationObject.id + "\nData: " + metaInformationObject.data + "\nOrigin: " + metaInformationObject.origin + "\nView-Count: " + str(metaInformationObject.viewCount) + "\n")   
        tagString = ""
    print("Record count: " + str(len(metaInformationObjectList)))
    Run()   
 
def CreateRandomId():
    return hashlib.md5(str(datetime.datetime.now()).encode()).hexdigest()
    
def GetPornhubDatabase():
    global metaInformationObjectList
    return metaInformationObjectList         

##################################### H E L P E R #####################################
#
####### this function i used to create a dictionary file out of a old db system #######
#
# def Once():
#     fileList = os.listdir(os.getcwd()+"/static/data/__")
#     fileNameList = []
#     keyWordDictionaryFile = open(os.getcwd()+"/static/data/dictionarys/keyWordDictionary" ,"w")
#     for file in fileList:
#         fileNameList.append(re.sub(".txt", "", file))
#     for fileName in fileNameList:
#         keyWordDictionaryFile.writelines(fileName+"\n")
#
######################################################################################
#
############## this function i used to clean duplicates from my list #################
#
# def RemoveDuplicatesFromList(_list):
#     print(len(_list))
#     _list = list(dict.fromkeys(_list))
#     print(len(_list))
#
######################################################################################
#
############### this function checks for duplicates and removes them #################
############### it will take up to several hours depending on size   #################
#
# def ClearDuplicatesByVideoUrl():
#     global metaInformationObjectList
#     currentListLength = len(metaInformationObjectList)
#     command = input(str(currentListLength) + " records in database to check. This can take some time: ")
#     if command == "yes":
#         for i in range(currentListLength):
#             print("OuterLoop-Index: " + str(i) + " URL: " + metaInformationObjectList[i].videoUrl)
#             for h in range(currentListLength):
#                 print("InnerLoop-Index: " + str(h))
#                 if h < currentListLength-1:
#                     if metaInformationObjectList[i].videoUrl == metaInformationObjectList[h+1].videoUrl:
#                         print("Duplicate at line: " + str(h+1) + " URL: " + metaInformationObjectList[h+1].videoUrl)
#                         metaInformationObjectList.remove(metaInformationObjectList[h+1])
#                         currentListLength = len(metaInformationObjectList)
#                         print("Current List Length: " + str(currentListLength))
#             if i == currentListLength:
#                 command = input("Save: ")
#                 if command == "yes":
#                     SaveMetaInformationObjectList()
#                     return    
#
########################################################################################
#
def ModuleUpdate():
    print("Activate function first")
    # command = input("Did you make a backup and modified the function? ")
    # if command != "yes":
    #     return False
    # InitDB()
    # global metaInformationObjectList
    # newModuleList = []
    # for metaInformationObject in metaInformationObjectList:
    #     #newModule = modules.newModule()
    #     newModule = modules.MetaInformationObject()
    #     newModule.videoUrl = metaInformationObject.videoUrl
    #     newModule.videoTitle = metaInformationObject.videoTitle
    #     newModule.videoDuration = metaInformationObject.videoDuration
    #     newModule.rating = metaInformationObject.rating
    #     newModule.tagList = metaInformationObject.tagList
    #     newModule.thumbnailPath = metaInformationObject.thumbnailPath
    #     newModule.discription = metaInformationObject.discription
    #     newModule.id = metaInformationObject.id
    #     newModule.data = metaInformationObject.data
    #     newModule.upVotes = ""
    #     newModule.downVotes = ""
    #     newModule.categoryList = metaInformationObject.tagList
    #     newModule.origin = "pornhub"
    #     newModule.owner = ""
    #     newModule.createdOn = ""
    #     newModule.sponsor = ""
    #     newModule.commentObjectList = []
    #     newModule.viewCount = ""
    #     newModuleList.append(newModule)
    # metaInformationObjectList.clear()
    # metaInformationObjectList = newModuleList.copy()
    # print("Module updatet")
    # SaveMetaInformationObjectList()
    # return True
#
#############################################################################
#
##### I use this function to update a varible of ervery module in list ######
#
# def WriteVaribleValueToAllObjects():
#    global metaInformationObjectList
#    for metaInformationObject in metaInformationObjectList:
#        metaInformationObject.origin = "pornhub"
#    SaveMetaInformationObjectList()
#############################################################################
#
#############################################################################
#
##### I use this function combine to databases ######
#
def CombineDatabases():
    newDatabaseFile = open(os.getcwd()+"/newPornHubDatabase", "rb")
    newMetaInformationObjectList = pickle.load(newDatabaseFile)
    newDatabaseFile.close()
    currentDatabaseFile = open(os.getcwd()+"/data/databases/pornhubdb.db", "rb")
    currentDatabase = pickle.load(currentDatabaseFile)
    counter = len(newMetaInformationObjectList)
    for newMio in newMetaInformationObjectList:
        isNew = True
        for mio in currentDatabase:
            if mio.videoUrl == newMio.videoUrl:
                print("Duplication for: " + newMio.videoUrl)
                isNew = False
                break
        if isNew:
            currentDatabase.append(newMio)
        counter -= 1
        print("Entrys Left: " + str(counter))
    combinedDatabaseFile = open(os.getcwd()+"/combindePornHubDatabase", "wb")
    pickle.dump(currentDatabase, combinedDatabaseFile)
    combinedDatabaseFile.close()
#############################################################################

if __name__ == "__main__":
    #ModuleUpdate()
    CombineDatabases()
    Run() 