import requests, re, pickle, hashlib, datetime, os
from nJoyPorn import modules
from fake_headers import Headers

header = Headers(browser="chrome", os="win", headers=True)
metaInformationObjectList = []
hotexporntoonsPattern = "<div class=\"item\">\n\s?<a href=\"(.*)\">\n\s+?<div class=\"i_img\">\n\s+?<img src=\"\/static\/engine\/img\/load\.gif\" data-src=\"(.*)\" class(.*)\">(.*)\n\s*(.*)svg>\s?(\d*)(.*)\n\s*(.*)svg>\s?(\d?\d?:?\d?\d?)(.*)\n\s<\/div>\n\s<div class=\"i_info\">\n\s*<div class=\"title\">(.*)<\/div>"
hotexporntoonsTagPattern = "<\/div>\n\s+<div class=\"description\">Tags (.*)<\/div>\n\<\/div>"

def Run():
    command = input("Enter command: [-initdb, -printdb, -search, -long, -edit -help]")
    if command == "-initdb":
        InitDB()
        print("exporntoonsDatabase loaded with " + str(len(metaInformationObjectList)) + " records")
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
    if command == "-edit":
        InitDB()
        Edit()
    if command == "-remove":
        InitDB()
        RemoveMetaIformationObjectFromDatabase()
    if command == "-exit":
        exit()
    if command == "-help":
        print("Learn how to deal with the issue... I dont care")
        Run()
    if command == "-updateModule":
        ModuleUpdate()
    print("Unknown Command...")
    Run()

def Edit():
    global metaInformationObjectList
    command = input("Enter video id: ")
    metaInformationObject = GetMetaInformationObjectById(command)
    if metaInformationObject != "invalid":
        command = input("Enter new thumbnail-Url: ")
        if command != "":
            metaInformationObject.thumbnailPath = command
    
        
def RemoveMetaIformationObjectFromDatabase():
    global metaInformationObjectList
    command = input("Enter video id: ")
    metaInformationObject = GetMetaInformationObjectById(command)
    if metaInformationObject != "invalid":
        command = input("MetaInformationObject with id: " + metaInformationObject.id + " found\nYou want to delete it? ")
        if command == "y" or "-y" or "--y" or "yes" or "-yes" or "--yes":
            metaInformationObjectList.remove(metaInformationObject)
        
    
def GetMetaInformationObjectById(_id):
    global metaInformationObjectList
    for metaInformationObject in metaInformationObjectList:
        if metaInformationObject.id == _id:
            return metaInformationObject
    return "invalid"

def PrintMetaInformationObjectList():
    global metaInformationObjectList
    tagString = ""
    for metaInformationObject in metaInformationObjectList:
        for tag in metaInformationObject.tagList:
            if tagString != "":
                tagString += " " + tag
            if tagString == "":
                tagString += tag
        print("Video-Title: " + metaInformationObject.videoTitle + "\nVideo-Url: " + metaInformationObject.videoUrl + "\nVideo-Duration: " + metaInformationObject.videoDuration + "\nVideo-Thumbnail: " + metaInformationObject.thumbnailPath + "\nTag-List: " + tagString  + "\nID: " + metaInformationObject.id + "\nData: " + metaInformationObject.data + "\nOrigin: " + metaInformationObject.origin + "\nView-Count: " + str(metaInformationObject.viewCount) + "\n")  
        tagString = ""
    print("Record count: " + str(len(metaInformationObjectList)))
    Run() 

def EnterKeyWords():
    keywords = re.split("\s+", input("Enter keywords for search: "))
    pageCount = int(input("How many pages to search: "))
    if pageCount < 1 or pageCount == "":
        pageCount = 1
    searchString = ""
    for word in keywords:
        if searchString != "": 
            searchString += "%20"+word
        if searchString == "":
            searchString += word
    for page in range(pageCount):
        print("Extracting page: " + str(page))
        if page == 0:
            url = "https://hot.exporntoons.net/video/"+searchString
        if page != 0:
            url = "https://hot.exporntoons.net/video/"+searchString + "?p=" + str(page)
        ExtractDataFromSite(url)
    command = input("Save Data To DB? ")
    if command == "y":
        SaveMetaInformationObjectList()
    if command != "y":
        print("Dumping data")
    Run()

def LongScrape():
    command = input("Enter paramater: ")
    keyWordList = CreateDictionary(command)  
    lineToStart = input("Enter the line you want to start with: ")
    if lineToStart == "":
        lineToStart = 0
    #pageCount = int(input("Enter depth of search as integer (eg. 3): "))
    # if pageCount < 1:
    #     pageCount = 1
    pageCount = 1
    #keyWordList = CreateDictionary()
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
        searchString = re.sub("\s", "-", keyWord)
        for page in range(pageCount):
            print("Extracting page: " + str(page))
            if page == 0:
                url = "https://hot.exporntoons.net/video/"+searchString
                print("URL: " + url)
            if page != 0:
                url = "https://hot.exporntoons.net/video/"+searchString + "?p=" + str(page)
            ExtractDataFromSite(url)
            SaveMetaInformationObjectList()
        lineCounter += 1
    Run()

def CreateDictionary(_command):
    if _command == "":
        keyWordDictionary = open(os.getcwd()+ "/data/dictionarys/keyWordDictionary" , "r")
        lines = keyWordDictionary.readlines()
        return lines
    if _command == "-pornstar":
        pornStarDictionary = open(os.getcwd()+ "/data/dictionarys/pornStarNameDictionary" , "r")
        lines = pornStarDictionary.readlines()
        return lines
    if _command == "-pornstar -tagList":
        return AddTagsToPornStartSearchList()

def AddTagsToPornStartSearchList():
    tagList = input("Enter tag(s): ")
    pornStarNameFile = open(os.getcwd()+"/dictionarys/pornStarNameDictionary" , "r")
    pornStarNameList = pornStarNameFile.readlines()
    lines=[]
    for pornstar in pornStarNameList:
        line = pornstar
        line += tagList
        lines.append(line)
    return lines

def ExtractDataFromSite(_url):
    global metaInformationObjectList
    sourceCode = requests.get(_url, headers=header.generate()).text
    for match in re.finditer(hotexporntoonsPattern, sourceCode):
        metaInformationObject = modules.MetaInformationObject()
        videoUrl = "https://hot.exporntoons.net" + match.group(1)
        videoTitle = match.group(11)
        videoDuration = match.group(9)
        rating = "ka"
        thumbnailPath = match.group(2)
        if MetaInformationObejctDuplication(videoUrl) == False:
            metaInformationObject.videoUrl = videoUrl
            metaInformationObject.videoTitle = videoTitle
            metaInformationObject.rating = rating
            metaInformationObject.videoDuration = videoDuration
            metaInformationObject.thumbnailPath = thumbnailPath
            metaInformationObject.tagList = GrabTagList(videoUrl)
            if len(metaInformationObject.tagList) < 1:
                metaInformationObject.tagList = BackUpTagList(_url)
            metaInformationObject.id = CreateRandomId()
            metaInformationObject.origin = "hotexporntoons"
            if ValidMetaInformationObject(metaInformationObject) == True:
                metaInformationObjectList.append(metaInformationObject)

def BackUpTagList(_url):
    print("Using backup tag list build from input data")
    return re.split("%20", re.sub("\?p=\d", "", re.sub("https://hot.exporntoons.net/video/", "", _url)))    

def MetaInformationObejctDuplication(_vidoeUrl):
    global metaInformationObjectList
    for metaInformationobject in metaInformationObjectList:
        if _vidoeUrl == metaInformationobject.videoUrl:
            print("Duplication for: " + _vidoeUrl + " dumping data")
            return True
    return False   

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

def GrabTagList(_url):
    sourceCode = requests.get(_url).text
    print("URL: " + _url + "\nVideo page source code loaded")
    tagList = []
    try:
        result = re.search(hotexporntoonsTagPattern, sourceCode)
        tagList = re.split(",\s", result.group(1))
    except:
        print("no tags grabed from page")
    return tagList

def InitDB():
    if os.path.exists(os.getcwd()+"/data/databases/hotexporntoons.db"):
        LoadMetaInformationObjectList()
        return
    print("HOTEXPORNTOONS: No database file found")
    command = input("HOTEXPORNTOONS: Create a new file? ")
    if command == "yes":
        file = open(os.getcwd()+"/data/databases/hotexporntoons.db", "wb")
        file.close()
        Run()

def SaveMetaInformationObjectList():
    global metaInformationObjectList
    file = open(os.getcwd()+"/data/databases/hotexporntoons.db", "wb")
    pickle.dump(metaInformationObjectList, file)
    file.close()
    print("Database saved")
    
def LoadMetaInformationObjectList():
    if os.path.exists(os.getcwd()+"/data/databases/hotexporntoons.db"):
        global metaInformationObjectList
        file = open(os.getcwd()+"/data/databases/hotexporntoons.db", "rb")
        try:
            metaInformationObjectList = pickle.load(file)
            print("HOTEXPORNTOONS. database loaded")
        except:
            print("HOTEXPORNTOONS: No data in db or data is corrupted")
        file.close()
        return
    print("HOTEXPORNTOONS: Cant load database file")

def GetExPornToonsDatabase():
    global metaInformationObjectList
    return metaInformationObjectList 

def CreateRandomId():
    return hashlib.md5(str(datetime.datetime.now()).encode()).hexdigest()
  
############################# H E L P E R ##############################
#
# payload = {
#    
#             "mode": "async",
#             "function": "get_html",
#             "block_id": "list_videos_videos_list_search_result",
#             "q": "sperma schlucken",
#             "category_ids": "" ,
#             "sort_by": "",
#             "from_videos": "1",
#             "from_albums": "1",
#             "_": "11321685468"
#           }
########################################################################            
#
# keyWords = "sperma schlucken"
# nextPageNumber = "3"
# string = "{\"mode\":\"async\",\"function\":\"get_html\",\"block_id\":\"list_videos_videos_list_search_result\",\"q\":\""+keyWords+"\",\"category_ids\":\"\",\"sort_by\":\"\",\"form_videos\":\""+nextPageNumber+"\",\"form_albums\":\""+ nextPageNumber+"\",\"_\";\"\"}"
########################################################################
#
# def CreatePayload():
#     return None
#
########################################################################
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
    #     newModule.data = ""
    #     newModule.upVotes = ""
    #     newModule.downVotes = ""
    #     newModule.categoryList = metaInformationObject.tagList
    #     newModule.origin = "fapster"
    #     newModule.owner = ""
    #     newModule.createdOn = ""
    #     newModule.sponsor = ""
    #     newModule.commentObjectList = []
    #     newModule.viewCount = ""
    #     newModuleList.append(newModule)
    #     newModuleList.append(newModule)
    # metaInformationObjectList.clear()
    # metaInformationObjectList = newModuleList.copy()
    # print("Module updatet")
    # SaveMetaInformationObjectList()
    # return True
#
############################################################################
#
##### I use this function to update a varible of ervery module in list ######
#
# def WriteVaribleValueToAllObjects():
#    global metaInformationObjectList
#    for metaInformationObject in metaInformationObjectList:
#        metaInformationObject.origin = "fapster"
#    SaveMetaInformationObjectList()
#############################################################################
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


if __name__ == "__main__":
    Run()