import requests, pickle, os, time, re, sys, datetime
from btcpay import BTCPayClient
from nJoyPorn import userDatabase, database, communication, modules

url = "https://www.njoyporn.com/api"
key = "3f2c7eb473ca5ad83f94bc1346b6cba9"
invoiceList = []
pendingInvoicesList = []
paidInvoiceList = []

paidInvoiceListLenght = 0
pattern = "{\"invoiceid\":\"(.*)\";\"userid\":\"(.*)\";\"videoid\":\"(.*)\"}"


paidAndDeliverdList =  []
paidAndDeliveredListLenght = 0

def Run(_command):
    if _command == "":
        _command = input("Enter command: [-payment, -btcpay -listenLoop] ")
    if _command == "-payment":
        Payment()
    if _command == "-btcpay":
        _command = input("Enter command: [-createClient] ")
        if _command == "-createClient":
            CreateClient()
    if _command == "-listenLoop":
        InitAPI()

def InitAPI():
    LoadPaidAndDeliveredList()
    if len(userDatabase.userObjectList) < 1:
        userDatabase.Api_Call_LoadFullUsersList()
    LoopCheck()
    

#for testing
def Payment():
    userId = input("Enter user-Id: ")
    videoId = input("Enter video-Id: ")
    data = userId + "??" + videoId
    data = {"command":"paymentDone", "data":data, "key": key}    
    Post(data)
    
def Post(_data):
    print(requests.post(url, data=_data).text)


def CreateClient():
    if os.path.exists(os.getcwd()+"/api/pair.pair"):
        print("client exists")
        return 
    #client = BTCPayClient.create_client(host='http://192.168.2.115:9001', code="rnbrerC")
    client = BTCPayClient.create_client(host='http://niclethic.com', code="bUtdmE6")
    SaveClient(client)

def LoadClient():
    file = open(os.getcwd()+"/api/pair.pair", "rb")
    return pickle.load(file)

def ProcessPayments():
    return None

def SaveClient(_client):
    if os.path.exists(os.getcwd()+"/api/pair.pair"):
        print("file exists")
        return 
    file = open(os.getcwd()+"/api/pair.pair", "wb")
    pickle.dump(_client, file)

def BtcPayment(_userId, _videoId):
    client = LoadClient()
    metaInformationObject = database.GetMetaInformationObjectById(_videoId)
    print("BTCPAY: user-id >> " + _userId)
    newInvoice = client.create_invoice({"price": metaInformationObject.price, "currency": "USD", "posData": _userId, "itemDesc": _videoId})
    #invoiceList.append(newInvoice)
    print("DEBUG: newInvoice-url >> " + newInvoice['url'])
    print("DEBUG: newInvoice-userId >> " + newInvoice['posData'])
    print("DEBUG: newInvoice-videoId >> " + newInvoice['itemDesc'])
    return newInvoice

def CustomInvoice(_userId, _sellerId, _offerId):
    client = LoadClient()
    buyerUserObject = userDatabase.GetUserById(_userId)
    sellerUserObject = userDatabase.GetUserById(_sellerId)
    buyerUserName = buyerUserObject.username
    conversation = communication.LoadConversationIfExisiting(buyerUserName, sellerUserObject.username)
    for message in conversation.messageList:
        if message.offer != "":
            if message.offer.id == _offerId:
                newInvoice = client.create_invoice({"price": message.offer.offerPrice, "currency": "USD", "posData": _userId, "itemDesc": _offerId, "buyer":{"name":_sellerId}})
                return newInvoice
    #offer is in message
    #message ist in conversation
    #conversation is in user
    #i can get user name bye userobject
    #i can get userobject by id
    
    return

def SavePaidAndDeliverdList():
    global paidAndDeliverdList
    global paidAndDeliveredListLenght
    paidAndDeliveredListLenght = len(paidInvoiceList)
    file = open(os.getcwd()+"/api/_data/paidAndDeliveredList", "wb")
    pickle.dump(paidInvoiceList, file)
    #print("API: Saved paidInvoiceList")


def LoadPaidAndDeliveredList():
    global paidAndDeliverdList
    global paidAndDeliveredListLenght
    if os.path.exists(os.getcwd()+"/api/_data/paidAndDeliveredList") == False:
        command = input("API: No database file found: Create one? ")
        if command == "yes":
            open(os.getcwd()+"/api/_data/paidAndDeliveredList", "wb")
    file = open(os.getcwd()+"/api/_data/paidAndDeliveredList", "rb")
    try:
        paidAndDeliverdList = pickle.load(file)
        paidAndDeliveredListLenght = len(paidAndDeliverdList)
    except:
        print("API: no data in paidAndDeliveredList")

def LoopCheck():
    run = True
    client = LoadClient()
    global paidAndDeliverdList
    global paidAndDeliveredListLenght
    tempPaidList = []
    fullList = []
    while run:
        tempPaidList.clear()
        fullList.clear()
        #time.sleep(2)
        fullList = client.get_invoices()
        print("API: Grabing data from server")
        print("DEBUG: templist >> " + str(len(tempPaidList)) + " tempPaidList >> " + str(len(fullList)) +" paidAndDeliverdList >> "+ str(len(paidAndDeliverdList)))
        #time.sleep(2)
        match = False
        for invoice in fullList:
            if invoice['status'] == "complete":
                tempPaidList.append(invoice)
        for invoice in tempPaidList:
            match = False
            if len(paidAndDeliverdList) < 1:
                Deliver(invoice['id'], invoice['posData'], invoice['itemDesc'])
                paidAndDeliverdList.append(invoice)
            for completedInvoice in paidAndDeliverdList:
                if invoice['id'] == completedInvoice['id']:
                    match = True
            if match == False:
                #print("DEBUG: invoice[\"buyer\"][\"name\"] >> " + invoice["buyer"]["name"])
                if invoice["buyer"]["name"] != None:
                    print("DELIVER EXTRA: " + invoice["buyer"]["name"])
                    CustomOfferGotPayed(invoice['id'], invoice['posData'], invoice['itemDesc'], invoice["buyer"]["name"])
                else:
                    Deliver(invoice['id'], invoice['posData'], invoice['itemDesc'])
                paidAndDeliverdList.append(invoice)
        if len(paidAndDeliverdList) > paidAndDeliveredListLenght + 1:
            SavePaidAndDeliverdList()
        print("API: Next round starts in 10 seconds...")
        time.sleep(10)

# def Check():
#     run = True
#     client = LoadClient()
#     global paidAndDeliverdList
#     global paidAndDeliveredListLenght
#     tempPaidList = []
#     fullList = []
#     #while run:
#     tempPaidList.clear()
#     fullList.clear()
#     #time.sleep(2)
#     fullList = client.get_invoices()
#     #print("API: Grabing data from server")
#     #print("DEBUG: templist >> " + str(len(tempPaidList)) + " tempPaidList >> " + str(len(fullList)) +" paidAndDeliverdList >> "+ str(len(paidAndDeliverdList)))
#     #time.sleep(2)
#     match = False
#     for invoice in fullList:
#         if invoice['status'] == "complete":
#             tempPaidList.append(invoice)
#     for invoice in tempPaidList:
#         match = False
#         if len(paidAndDeliverdList) < 1:
#             Deliver(invoice['id'], invoice['posData'], invoice['itemDesc'])
#             paidAndDeliverdList.append(invoice)
#         for completedInvoice in paidAndDeliverdList:
#             if invoice['id'] == completedInvoice['id']:
#                 match = True
#         if match == False:
#             Deliver(invoice['id'], invoice['posData'], invoice['itemDesc'])
#             paidAndDeliverdList.append(invoice)
#     if len(paidAndDeliverdList) > paidAndDeliveredListLenght + 1:
#         SavePaidAndDeliverdList()
#     #print("API: Next round starts in 10 seconds...")
#     #time.sleep(10)

def CustomOfferGotPayed(_invoiceId, _userId, _itemId, _sellerId):
    print("_sellerId: " + _sellerId)
    print("_buyerId: " + _userId)
    sellerUserObject = userDatabase.GetUserById(_sellerId)
    buyerUserObject = userDatabase.GetUserById(_userId)
    sellerConversationFile = open(os.getcwd()+"/userDatabase/"+sellerUserObject.username+"/messages/"+buyerUserObject.username, "rb")
    sellerConversation = pickle.load(sellerConversationFile)
    sellerConversationFile.close()
    for message in sellerConversation.messageList:
        if message.offer != "":
            if message.offer.id == _itemId:
                newMessage = modules.Message()
                newMessage.senderNickName = "nJoyPorn-Support"
                newMessage.senderId = _sellerId
                newMessage.receiverId = _userId
                newMessage.messageText = "Your offer got accepted and payed in full"
                newMessage.senderUserName = sellerUserObject.username
                newMessage.receiverUserName = buyerUserObject.username
                newMessage.timeStamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
                newMessage.id = userDatabase.CreateRandomId()
                newMessage.conversationId = sellerConversation.id
                sellerConversation.messageList.append(newMessage)
                sellerConversationFile = open(os.getcwd()+"/userDatabase/"+sellerUserObject.username+"/messages/"+buyerUserObject.username, "wb")
                pickle.dump(sellerConversation, sellerConversationFile)
                sellerConversationFile.close()
    buyerConversationFile = open(os.getcwd()+"/userDatabase/"+buyerUserObject.username+"/messages/"+sellerUserObject.username, "rb")
    buyerConversation = pickle.load(buyerConversationFile)
    buyerConversationFile.close()
    for message in buyerConversation.messageList:
        if message.offer != "":
            if message.offer.id == _itemId:
                newMessage.senderNickName = "nJoyPorn-Support"
                newMessage.senderId = _userId
                newMessage.receiverId = _sellerId
                newMessage.messageText = "Your payment got accepted"
                newMessage.senderUserName = buyerUserObject.username
                newMessage.receiverUserName = sellerUserObject.username
                newMessage.conversationId = buyerConversation.id
                buyerConversation.messageList.append(newMessage)
                buyerConversationFile = open(os.getcwd()+"/userDatabase/"+buyerUserObject.username+"/messages/"+sellerUserObject.username, "wb")
                pickle.dump(buyerConversation, buyerConversationFile)
                buyerConversationFile.close()

def Deliver(_invoiceId, _userId, _itemId):
    if _invoiceId == None or _userId == None or _itemId == None:
        print("API: invalid invoice data!")
        return
    file = open(os.getcwd()+"/api/_data/__logs/log", "r")
    lines = file.readlines()
    file.close()
    for line in lines:
        result = re.search(pattern, line)
        if result.group(2) == _userId and result.group(3) == _itemId:
            print("user has the item bought earlier i guess ?")
            return
    API_AddVideoToPurchasedList(_userId, _itemId)
    file = open(os.getcwd()+"/api/_data/__logs/log", "a")
    line = "{\"invoiceid\":\""+_invoiceId+"\";\"userid\":\""+_userId+"\";\"videoid\":\""+_itemId+"\"}"
    file.write(line+"\n")
    print("API: Delivered invoiceid >> " + _invoiceId + " userid >> " + _userId + " videoid >> " + _itemId)        

def API_AddVideoToPurchasedList(_userId, _itemId):
    data = _userId + "??" + _itemId
    data = {"command":"paymentDone", "data":data, "key": key}    
    API_Post(data)
    
def API_Post(_data):
    requests.post(url, data=_data)
        
# def Deliver_(_invoiceId, _userId, _itemId):
#     if _invoiceId == None or _userId == None or _itemId == None:
#         print("API: invalid invoice data!")
#         return
#     file = open(os.getcwd()+"/api/_data/__logs/log", "r")
#     lines = file.readlines()
#     file.close()
#     for line in lines:
#         result = re.search(pattern, line)
#         if result.group(2) == _userId and result.group(3) == _itemId:
#             print("user has the item bought earlier i guess ?")
#             return
#     userDatabase.AddVideoToPurchasedList(_userId, _itemId)
#     file = open(os.getcwd()+"/api/_data/__logs/log", "a")
#     line = "{\"invoiceid\":\""+_invoiceId+"\";\"userid\":\""+_userId+"\";\"videoid\":\""+_itemId+"\"}"
#     file.write(line+"\n")
#     print("API: Delivered invoiceid >> " + _invoiceId + " userid >> " + _userId + " videoid >> " + _itemId)
                
if __name__ == "__main__":
    #InitAPI() #Loads data and starts the loop for manage invoices
    try:
        command = sys.argv[1]
    except:
        command = ""
    Run(command)
    