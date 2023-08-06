import os, re, datetime, hashlib, pickle
from nJoyPorn import database, modules

analyticalObjectList = []
keyWordListList = []
categorieAnalyticObjectList = []
pornStarAnalyticObjectList = []

def Run():
    command = input("Enter command: [-initdb, -print, -help -countCodeLines]")
    if command == "-initdb":
        InitDB()
        Run()
    if command == "-print":
        command = input("Enter command: [-video, -keyWords, -categorie, -pornstar] ")
        if command == "-video":
            print(end="", flush=True)
            PrintVideoData()
        if command == "-keyWords":
            print(end="", flush=True)
            PrintKeyWordListList()
        if command == "-categorie":
            PrintCategorieAnalytics()
        if command == "-pornstar":
            PrintPornPornstarAnalytics()
    if command == "-help":
        print(end="", flush=True)
        print("This is the help page for gilltrickdb:\n You can enter these commands:\n --initdb: this initializes the database its like reloading\n --help: Prints this page")
        input("Press Enter to exit help")
        Run()
    if command == "-countCodeLines":
        CountLines()
    if command == "-exit":
        exit()

def InitDB():
    LoadAnalyticalObjectList()
    LoadKeyWordListList()
    LoadCategorieAnalyticObjectList()
    LoadPornStarAnalyticObjectList()
    
def LoadAnalyticalObjectList():
    if os.path.exists(os.getcwd()+"/data/analytics/analytics.db"):
        global analyticalObjectList
        file = open(os.getcwd()+"/data/analytics/analytics.db", "rb")
        try:
            analyticalObjectList = pickle.load(file)
            print("ANALYTICS: AnalyticalObjectList loaded")
            file.close()
        except:
            print("ANALYTICS: Can't load analytics database")
            file.close()
    
def SaveAnalyticalObjectList():
    global analyticalObjectList
    file = open(os.getcwd()+"/data/analytics/analytics.db", "wb")
    pickle.dump(analyticalObjectList, file)
    file.close()

def LoadKeyWordListList():
    global keyWordListList
    if os.path.exists(os.getcwd()+"/data/analytics/keyWordList.db"):
        keyWordListListFile = open(os.getcwd()+"/data/analytics/keyWordList.db", "r").readlines()
        for line in keyWordListListFile:
            keyWordListList.append(re.split(",\s", line))
        print("ANALYTICS: Loaded keyWordList" )
        return
    print("ANALYTICS: Can't load keyWordList.db")

def SaveKeyWordList(_keyWordList):
    global keyWordListList
    keyWordListList.append(_keyWordList)
    #try to save file
    line = "";
    for keyWord in _keyWordList:
        if line != "":
            line += ", " + keyWord
        if line == "":
            line += keyWord
    try:
        keyWordFile = open(os.getcwd()+"/data/analytics/keyWordList.db", "a")
        keyWordFile.write(line+"\n")
        keyWordFile.close()
        print("ANALYTICS: keyWordList.db updated")
    except:
        print("ANALYTICS: Can't update keyWordList.db. probably not an issue")
      
def LoadCategorieAnalyticObjectList():
    global categorieAnalyticObjectList
    if os.path.exists(os.getcwd()+"/data/analytics/categorieAnalytics.db"):
        try:
            categorieAnalyticObjectListFile = open(os.getcwd() + "/data/analytics/categorieAnalytics.db", "rb")
            try:
                categorieAnalyticObjectList = pickle.load(categorieAnalyticObjectListFile)
                categorieAnalyticObjectListFile.close()
            except:
                print("ANALYTICS: No valid data in categorieAnalytics.db file")
        except:
            print("ANALYTICS: Can't load categorieAnalytics.db, does the file exist?")
            return
    print("ANALYTICS: categorieAnalytics.db loaded")

def SaveCategorieAnalyticObjectList():
    global categorieAnalyticObjectList
    if os.path.exists(os.getcwd()+"/data/analytics/categorieAnalytics.db"):
        categorieAnalyticObjectListFile = open(os.getcwd() + "/data/analytics/categorieAnalytics.db", "wb")
        pickle.dump(categorieAnalyticObjectList, categorieAnalyticObjectListFile)
        categorieAnalyticObjectListFile.close()
        print("ANALYTICS: categoryAnalytics database saved")

def LoadPornStarAnalyticObjectList():
    global pornStarAnalyticObjectList
    if os.path.exists(os.getcwd()+"/data/analytics/pornStarAnalytics.db"):
        try:
            pornStarAnalyticObjectListFile = open(os.getcwd() + "/data/analytics/pornStarAnalytics.db", "rb")
            try:
                pornStarAnalyticObjectList = pickle.load(pornStarAnalyticObjectListFile)
                pornStarAnalyticObjectListFile.close()
            except:
                print("ANALYTICS: No data valid data in pornStarAnalytics.db file")
        except:
            print("ANALYTICS: Can't load pornStarAnalytics.db, does the file exist?")
            return

    print("ANALYTICS: pornStarAnalytics.db loaded")        

def SavePornStarAnalyticObjectList():
    global pornStarAnalyticObjectList
    if os.path.exists(os.getcwd()+"/data/analytics/pornStarAnalytics.db"):
        pornStarAnalyticObjectListFile = open(os.getcwd() + "/data/analytics/pornStarAnalytics.db", "wb")
        pickle.dump(pornStarAnalyticObjectList, pornStarAnalyticObjectListFile)
        pornStarAnalyticObjectListFile.close()
        print("ANALYTICS: pornStarAnalytics database saved")

def UpdatePornStarObject(_pornStarName):
    global pornStarAnalyticObjectList
    for pornStarAnalyticObject in pornStarAnalyticObjectList:
        if _pornStarName == pornStarAnalyticObject.name:
            pornStarAnalyticObject.counter += 1
            print(("ANALYTICS: categorieAnalyticsObject: " + pornStarAnalyticObject.name + " in categoryAnalytics database updated."))
            SavePornStarAnalyticObjectList()

def UpdateCategoryObject(_categoryName):
    global categorieAnalyticObjectList
    for categorieAnalyticObject in categorieAnalyticObjectList:
        if _categoryName == categorieAnalyticObject.name:
            categorieAnalyticObject.counter += 1
            print(("ANALYTICS: categorieAnalyticsObject: " + categorieAnalyticObject.name + " in categoryAnalytics database updated."))
            SaveCategorieAnalyticObjectList()
            
def AnalyticalObjectExits(_url):
    global analyticalObjectList
    for analyticalObject in analyticalObjectList:
        if analyticalObject.metaInformationObject.videoUrl == _url:
            analyticalObject.watchCounter += 1
            SaveAnalyticalObjectList()
            #append data
            return
    NewAnalyticalObject(_url)
    
def NewAnalyticalObject(_url):
    newAnalyticalObject = modules.AnaltycisObject()
    metaInformationObject = database.GetMetaInfromationObjectByVideoUrl(_url)
    try:
        if metaInformationObject.videoUrl == "":
            print("ANALYTICS: No metaInformationObject from database loaded")
            return
        if metaInformationObject.videoUrl != "":
            newAnalyticalObject.metaInformationObject = metaInformationObject
            newAnalyticalObject.watchCounter = 1
            newAnalyticalObject.id = CreateRandomId()
            analyticalObjectList.append(newAnalyticalObject)
            database.LoadPopularPornStarList()
            database.LoadPopularCategoryList()
            SaveAnalyticalObjectList()
            return
    except:
            print("ANALYTICS: No metaInformationObject from database loaded")
            return        
            
def AnalyseKeyWords():
    global keyWordListList
    tempListList = keyWordListList.copy()
    _kwList = []
    for keyWordList in tempListList:
        for keyWord in keyWordList:
            if keyWord not in _kwList():
                _kwList.append(keyWord)

def PrintCategorieAnalytics():
    global categorieAnalyticObjectList
    command = input("Choose option:\n (1) print all categorie names\n (2) print data of categorie by name\n (3) print categorie names sorted by view count\n (4) search and print categorie data\n Enter number: ")
    if command == "1":
        for categorieAnalyticObject in categorieAnalyticObjectList:
            print("Categorie-Name: " + categorieAnalyticObject.name)
        PrintCategorieAnalytics()
    if command == "2":
        nameList = []
        alphabeticalSortedCategorieAnalyticObjectList = []
        for categorieAnalyticObject in categorieAnalyticObjectList: 
            nameList.append(categorieAnalyticObject.name)
        nameList.sort()
        for name in nameList:
            for categorieAnalyticObject in categorieAnalyticObjectList:
                if categorieAnalyticObject.name == name:
                    alphabeticalSortedCategorieAnalyticObjectList.append(categorieAnalyticObject)
        for categorieAnalyticObject in alphabeticalSortedCategorieAnalyticObjectList:
            print("Category-Name: " + categorieAnalyticObject.name + "\nView-Count: " + str(categorieAnalyticObject.counter)+"\n")
        PrintCategorieAnalytics()
    if command == "3":
        tempList = categorieAnalyticObjectList.copy()
        counterList = []
        sortedCategoryAnalyticObjectList = []
        for categorieAnalyticObject in tempList:
            counterList.append(categorieAnalyticObject.counter)
        counterList.sort()
        for counter in counterList:
            for categorieAnalyticObject in tempList:
                if categorieAnalyticObject.counter == counter:
                    sortedCategoryAnalyticObjectList.append(categorieAnalyticObject)
                    tempList.remove(categorieAnalyticObject)
        #by this i get the first value in the list with the smallest counter. its easier to read in print :D
        for obj in sortedCategoryAnalyticObjectList:
            print("Name: " + obj.name + "\nCounter: " + str(obj.counter) + "\n")
        PrintCategorieAnalytics()
    if command == "4":
        command = input("Enter category name: ")
        for categorieAnalyticObject in categorieAnalyticObjectList:
            if categorieAnalyticObject.name == command:
                print("Category-Name: " + categorieAnalyticObject.name + "\nView-Count: " + str(categorieAnalyticObject.counter))
                PrintCategorieAnalytics()
        print("ANALYTICS: Categorie name not found")
        PrintCategorieAnalytics()
    if command == "-return":
            Run()
    if command == "-exit":
        exit()

def PrintPornPornstarAnalytics():
    global pornStarAnalyticObjectList
    print(str(len(pornStarAnalyticObjectList)))
    command = input("Choose option:\n (1) print all pornStar names\n (2) print data of pornStar by name\n (3) print pornStar names sorted by view count\n (4) search and print porn star by name\n Enter number: ")
    if command == "1":
        for pornStarAnalyticObject in pornStarAnalyticObjectList:
            print("PornStar-Name: " + pornStarAnalyticObject.name)
        PrintPornPornstarAnalytics()
    if command == "2":
        nameList = []
        alphabeticalSortedPornStarAnalyticObjectList = []
        for pornStarAnalyticObject in pornStarAnalyticObjectList: 
            nameList.append(pornStarAnalyticObject.name)
        nameList.sort()
        for name in nameList:
            for pornStarAnalyticObject in pornStarAnalyticObjectList:
                if pornStarAnalyticObject.name == name:
                    alphabeticalSortedPornStarAnalyticObjectList.append(pornStarAnalyticObject)
        for pornStarAnalyticObject in alphabeticalSortedPornStarAnalyticObjectList:
            print("Category-Name: " + pornStarAnalyticObject.name + "\nView-Count: " + str(pornStarAnalyticObject.counter)+"\n")
        PrintPornPornstarAnalytics()
    if command == "3":
        tempList = pornStarAnalyticObjectList.copy()
        counterList = []
        sortedCategoryAnalyticObjectList = []
        for pornStarAnalyticObject in tempList:
            counterList.append(pornStarAnalyticObject.counter)
        counterList.sort()
        for counter in counterList:
            for pornStarAnalyticObject in tempList:
                if pornStarAnalyticObject.counter == counter:
                    sortedCategoryAnalyticObjectList.append(pornStarAnalyticObject)
                    tempList.remove(pornStarAnalyticObject)
        #by this i get the first value in the list with the smallest counter. its easier to read in print :D
        for obj in sortedCategoryAnalyticObjectList:
            print("Name: " + obj.name + "\nCounter: " + str(obj.counter) + "\n")
        PrintPornPornstarAnalytics()
    if command == "4":
        command = input("Enter category name: ")
        for pornStarAnalyticObject in pornStarAnalyticObjectList:
            if pornStarAnalyticObject.name == command:
                print("Category-Name: " + pornStarAnalyticObject.name + "\nView-Count: " + str(pornStarAnalyticObject.counter))
                PrintCategorieAnalytics()
        print("ANALYTICS: Categorie name not found")
        PrintCategorieAnalytics()
    if command == "-return":
            Run()
    if command == "-exit":
        exit()
            
def PrintVideoData():
    global analyticalObjectList
    for analyticalObject in analyticalObjectList:
        print("Video-Title: " + analyticalObject.metaInformationObject.videoTitle + "\nWatch-Counter: " + str(analyticalObject.watchCounter)+"\n")
    print("Records count: " + str(len(analyticalObjectList)))
        
def PrintKeyWordListList():
    global keyWordListList
    for keyWordList in keyWordListList:
        for keyWord in keyWordList:
            print("Keyword: " + keyWord)  

def CreatePornStarNameList():   
    file = open(os.getcwd()+"/data/dictionarys/categorieDictionary")
    lines = file.readlines()
    tempList = []
    for line in lines:
        line = re.sub("\n", "", line)
        tempList.append(line)
    return tempList

def LoadPopularCategorieList():
    global categorieAnalyticObjectList
    popularCategoriesList = []
    tempList = categorieAnalyticObjectList.copy()
    counterList = []
    sortedCategorieAnalyticObjectList = []
    for categorieAnalyticObject in tempList:
        counterList.append(categorieAnalyticObject.counter)
    counterList.sort()
    for counter in counterList:
        for categorieAnalyticObject in tempList:
            if categorieAnalyticObject.counter == counter:
                sortedCategorieAnalyticObjectList.append(categorieAnalyticObject)
                tempList.remove(categorieAnalyticObject)
    counter = 0
    for categorieAnalyticObject in sortedCategorieAnalyticObjectList:
        if counter < 32:
            popularCategoriesList.append(categorieAnalyticObject)
            couter += 1
    return popularCategoriesList

def LoadPopularPornStarList():
    global pornStarAnalyticObjectList
    popularPornStarsList = []
    tempList = pornStarAnalyticObjectList.copy()
    counterList = []
    sortedPornStarAnalyticObjectList = []
    for pornStarAnalyticObject in tempList:
        counterList.append(pornStarAnalyticObject.counter)
    counterList.sort()
    for counter in counterList:
        for pornStarAnalyticObject in tempList:
            if pornStarAnalyticObject.counter == counter:
                sortedPornStarAnalyticObjectList.append(pornStarAnalyticObject)
                tempList.remove(pornStarAnalyticObject)
    counter = 0
    for pornStarAnalyticObject in sortedPornStarAnalyticObjectList:
        if counter < 32:
            popularPornStarsList.append(pornStarAnalyticObject)
            couter += 1
    return popularPornStarsList
          
def CreateRandomId():
    return hashlib.md5(str(datetime.datetime.now()).encode()).hexdigest()

####################### i use this function to create a list of  category object from dictionary #######################
def CreateNewCategorieAnalyticObjectListFromCategorieDictionary():
    print("Activate the function in code: RETURN")
    return
    # global categorieAnalyticObjectList
    # try:
    #     file = open(os.getcwd()+"/static/data/dictionarys/categorieDictionary", "r")
    # except:
    #     print("ANALYTICS: Can't load categoryDictionary file")
    #     return
    # lines = file.readlines()
    # tempList = []
    # for line in lines:
    #     line = re.sub("\n", "", line)
    #     tempList.append(line)
    # counter = 0
    # if os.path.exists(os.getcwd()+"/static/data/analytics/categorieAnalytics.db"):
    #     for categorieName in tempList:
    #         counter += 1
    #         categorieAnalyticObject = modules.CategoryAnalyticsObject()
    #         categorieAnalyticObject.categorieId = str(counter)
    #         categorieAnalyticObject.name = categorieName
    #         categorieAnalyticObject.id = CreateRandomId()
    #         categorieAnalyticObject.createdOn = str(datetime.datetime.now())
    #         categorieAnalyticObject.lastUpdate = categorieAnalyticObject.createdOn
    #         categorieAnalyticObject.searchTermCharts = modules.CategoryAnalyticsObject.SearchTermChartList()
    #         categorieAnalyticObjectList.append(categorieAnalyticObject)
    #     SaveCategorieAnalyticObjectList()
    #     print("ANALYTICS: categoryAnalyticsObjectList created from dictionary")
    #     return
    # print("ANALYTICS: Can't load categorieAnalytics.db, does the file exist?")
    
def CreateNewPornStarAnalyticsObjectListFromPornStarNameDictionary():
    print("Activate the function in code: RETURN")
    return
    # global pornStarAnalyticObjectList
    # try:
    #     file = open(os.getcwd()+"/static/data/dictionarys/pornStarNameDictionary", "r")
    # except:
    #     print("ANALYTICS: Can't load categoryDictionary file")
    #     return
    # lines = file.readlines()
    # tempList = []
    # for line in lines:
    #     line = re.sub("\n", "", line)
    #     tempList.append(line)
    # counter = 0
    # if os.path.exists(os.getcwd()+"/static/data/analytics/pornStarAnalytics.db"):
    #     for pornStarName in tempList:
    #         counter += 1
    #         pornStarAnalyticObject = modules.PornStarAnalyticsObject()
    #         pornStarAnalyticObject.categorieId = str(counter)
    #         pornStarAnalyticObject.name = pornStarName
    #         pornStarAnalyticObject.id = CreateRandomId()
    #         pornStarAnalyticObject.createdOn = str(datetime.datetime.now())
    #         pornStarAnalyticObject.lastUpdate = pornStarAnalyticObject.createdOn
    #         pornStarAnalyticObject.searchTermCharts = modules.CategoryAnalyticsObject.SearchTermChartList()
    #         pornStarAnalyticObjectList.append(pornStarAnalyticObject)
    #     SavePornStarAnalyticObjectList()
    #     print("ANALYTICS: pornstarAnalyticsObjectList created from dictionary")
    #     return
    # print("ANALYTICS: Can't load categorieAnalytics.db, does the file exist?")

def CountLines():
    counter = 0
    pyList = os.listdir(os.getcwd())
    htmlList = os.listdir(os.getcwd()+"/templates")
    cssList = os.listdir(os.getcwd()+"/static/styles")
    jsList = os.listdir(os.getcwd()+"/static/js")
    counter = 0
    for file in pyList:
        if ".py" in file:
            counter += len(open(os.getcwd()+"/"+file).readlines())
    for file in htmlList:
        counter += len(open(os.getcwd()+"/templates/"+file).readlines())
    for file in cssList:
        if "fonts" not in file:
            counter += len(open(os.getcwd()+"/static/styles/"+file).readlines())
    for file in jsList:
        counter += len(open(os.getcwd()+"/static/js/"+file).readlines())
    print(counter)

     
if __name__ == "__main__":
    Run()
