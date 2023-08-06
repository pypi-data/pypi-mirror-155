import os, pickle, hashlib, datetime
from nJoyPorn import modules, userDatabase

messageRoot = os.getcwd()+"/userDatabase/"

conversationList = []

def SendMessage(_senderId, _receiverId, _senderUserName, _titleText, _messageText, _senderNickName):
    timeStamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    receiverUserName = userDatabase.GetUserById(_receiverId).username 
    message = modules.Message.CreateMessage(_senderId, _receiverId, _senderUserName, receiverUserName, _titleText, _messageText, timeStamp, _senderNickName)
    message.id = CreateRandomId()
    if ConversationExists(message):
        UpdateConversation(message)
        return
    return StartConversation(message)

    
def ConversationExists(_message):
    if os.path.exists(messageRoot+"/"+_message.senderUserName+"/messages/"+_message.receiverUserName):
        return True
    
def UpdateConversation(_message):
    senderConversationFile = open(messageRoot+"/"+_message.senderUserName+"/messages/"+_message.receiverUserName, "rb")
    senderConversation = pickle.load(senderConversationFile)
    senderConversationFile.close()
    _message.conversationId = senderConversation.id
    senderConversation.participentId = _message.receiverId
    senderConversation.senderUserName = _message.senderUserName
    senderConversation.receiverUserName = _message.receiverUserName
    senderConversation.participentNickName = userDatabase.GetUserById(_message.receiverId).nickName
    senderConversation.messageList.append(_message)
    senderFile = open(messageRoot+"/"+_message.senderUserName+"/messages/"+_message.receiverUserName,"wb")
    pickle.dump(senderConversation, senderFile)
    senderFile.close()
    receiverConversationFile = open(messageRoot+"/"+_message.receiverUserName+"/messages/"+_message.senderUserName,"rb")
    receiverConversation = pickle.load(receiverConversationFile)
    receiverConversationFile.close()
    receiverConversation.participentId = _message.senderId
    receiverConversation.senderUserName = _message.receiverUserName
    receiverConversation.receiverUserName = _message.senderUserName
    receiverUserObject = userDatabase.GetUserById(_message.receiverId)
    receiverUserObject.unreadConversationsList.append(senderConversation.id)
    userDatabase.SaveUserData(receiverUserObject)
    receiverConversationFile.participentNickName = receiverUserObject.nickName
    receiverConversation.messageList.append(_message)
    receiverConversationFile = open(messageRoot+"/"+_message.receiverUserName+"/messages/"+_message.senderUserName,"wb")
    pickle.dump(receiverConversation, receiverConversationFile)  
    receiverConversationFile.close()

    
def StartConversation(_message):
    conversation = modules.Conversation()
    conversation.id = CreateRandomId()
    conversation.starterId = _message.senderId
    conversation.participentId = _message.receiverId
    conversation.senderUserName = _message.senderUserName
    conversation.receiverUserName = _message.receiverUserName
    conversation.participentNickName = userDatabase.GetUserById(_message.receiverId).nickName
    conversation.messageList.append(_message)
    senderFile = open(messageRoot+"/"+_message.senderUserName+"/messages/"+conversation.receiverUserName,"wb")
    pickle.dump(conversation, senderFile)
    senderFile.close()
    receiverFile = open(messageRoot+"/"+_message.receiverUserName+"/messages/"+conversation.senderUserName,"wb")
    conversation.participentId = _message.senderId
    conversation.senderUserName = _message.receiverUserName
    conversation.receiverUserName = _message.senderUserName
    participentUserObject = userDatabase.GetUserById(_message.receiverId)
    participentUserObject.unreadConversationsList.append(conversation.id)
    userDatabase.SaveUserData(participentUserObject)
    conversation.participentNickName = userDatabase.GetUserById(_message.senderId).nickName
    pickle.dump(conversation, receiverFile)  
    receiverFile.close()
    conversationList.append(conversation)
    userDatabase.SaveUserData(participentUserObject)
    return conversation

def MarkConversationAsRead(_conversationId, _userId):
    userObject = userDatabase.LoadUserObjectById(_userId)
    userObject.unreadConversationsList.remove(_conversationId)
    userDatabase.SaveUserData(userObject)
    return

def CreateOffer(_sellerId, _buyerId, _offerTitle, _offerText, _offerPrice):
    sellerUserObject = userDatabase.LoadUserObjectById(_sellerId)
    receiverUserObject = userDatabase.LoadUserObjectById(_buyerId)
    timeStamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    offer = modules.CustomSale()
    offer.id = CreateRandomId()
    offer.sellerId = _sellerId
    offer.buyerId = _buyerId
    offer.offerTitle = _offerTitle
    offer.offerText = _offerText
    offer.offerPrice = _offerPrice
    offer.timeStamp = timeStamp
    message = modules.Message.CreateMessage(_sellerId, _buyerId, sellerUserObject.username, receiverUserObject.username, "offerMessage", "", timeStamp, sellerUserObject.nickName)
    message.id = CreateRandomId()
    message.offer = offer
    SendOfferMessage(message)

    
def SendOfferMessage(_message):
    #receiverUserName = userDatabase.GetUserById(_receiverId).username 
    #message = modules.Message.CreateMessage(_senderId, _receiverId, _senderUserName, receiverUserName, _titleText, _messageText, timeStamp, _senderNickName)
    #message.id = CreateRandomId()
    if ConversationExists(_message):
        UpdateConversation(_message)
        return
    StartConversation(_message)    
    
def SendFollowerNotificationMessage(_message):
    if ConversationExists(_message):
        UpdateConversation(_message)
        return
    StartConversation(_message)  
        
def LoadUsersConversations(_username):
    conversationFileNameList = os.listdir(messageRoot+"/"+_username+"/messages/")
    conversationList = []
    for conversationFileName in conversationFileNameList:
        conversationFile = open(messageRoot+"/"+_username+"/messages/"+conversationFileName, "rb")
        conversation = pickle.load(conversationFile)
        conversationList.append(conversation)
    return conversationList
           
def LoadConversationIfExisiting(_username, _receiverUserName):
    if os.path.exists(messageRoot+"/"+_username+"/messages/"+_receiverUserName):
        conversationFile = open(messageRoot+"/"+_username+"/messages/"+_receiverUserName, "rb")
        conversation = pickle.load(conversationFile)
        conversationFile.close()
        return conversation
    return None

def CreateRandomId():
    return hashlib.md5(str(datetime.datetime.now()).encode()).hexdigest()

    
def CreateDummyConversation():
    #make this the welcome message and entry point for writing with the support 
    # i have to create a conversation and save it for both
    conversation = modules.Conversation()
    conversation.participentNickName = "Dummy-Object"
    message = modules.Message()
    message.titleText = "Dummy-Message"
    message.messageText = "Dummy-Message-Text-Content"
    conversation.messageList.append(message)
    return conversation

def CreateSupportConversation(_userId):
    receiverUserObject = userDatabase.LoadUserObjectById(_userId)
    senderId = "09a3401a97098f7257a81c8502236340"
    senderUsername = "d338b3f0f405eb5e51c8cc1e5ca66f02"
    titleText = "Hello and welcome to nJoyPorn"
    messageText = "You can answer on this messag in case you need some support :)"
    senderNickName = "Support"
    return SendMessage(senderId, receiverUserObject.id, senderUsername, titleText, messageText, senderNickName)
    
def NotifyFollower(_userObject, __metaInformationObject):
    for follower in _userObject.followerList:
        followerUserObject = userDatabase.LoadUserObjectById(follower)
        message = modules.Message()
        message.titleText = "followerNotification"
        message.messageText = "My new viedeo: " + __metaInformationObject.videoTitle + " is online"
        message.offer = __metaInformationObject.videoUrl
        message.id = CreateRandomId()
        message.senderId = _userObject.id
        message.senderUserName = _userObject.username
        message.senderNickName = _userObject.nickName
        message.receiverId = follower
        message.receiverUserName = followerUserObject.username
        message.timeStamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        #SendMessage(_userObject.id, follower, _userObject.username, "followerNotification", "My new viedeo: " + __metaInformationObject.videoTitle + " is online", _userObject.nickName)
        SendFollowerNotificationMessage(message)
    return