class MetaInformationObject:
    def __init__(self):
        self.videoUrl = ""
        self.videoTitle = ""
        self.videoDuration = ""
        self.rating = 0
        self.tagList = []
        self.thumbnailPath = ""
        self.discription = ""
        self.id = ""
        self.data = ""
        self.upVotes = 0
        self.downVotes = 0
        self.categoryList = []
        self.origin = ""
        self.owner = ""
        self.createdOn = ""
        self.sponsor = ""
        self.commentObjectList = []
        self.viewCount = 0
        self.price = 0
        self.currency = ""
        self.favoriteCounter = 0
        self.sellCounter = 0
        self.sellVideoId = ""
        self.trailerId = ""
        self.videoType = ""
        self.fileName = ""
        
class DataBaseFile:
    def __init__(self):
        self.MetaInformationObjectList = []

class CommentObject:
    def __init__(self):
        self.text = ""
        self.writerId = ""
        self.writerNickName = ""
        self.createdOn = ""
        self.upVotes = ""
        self.downVotes = ""
        self.id = ""
        self.metaInformatinoObjectId = ""
        self.videoUrl = ""
        self.videoThumbnailUrl = ""
################################## H E L P E R ####################################
#        
# class newModule:
#     def __init__(self):
#         self.videoUrl = ""
#         self.videoTitle = ""
#         self.videoDuration = ""
#         self.rating = 0
#         self.tagList = []
#         self.thumbnailPath = ""
#         self.discription = ""
#         self.id = ""
#         self.data = ""
#         self.upVotes = 0
#         self.downVotes = 0
#         self.categoryList = []
#         self.origin = ""
#         self.owner = ""      
#         self.createdOn = ""
#         self.sponsor = ""
#         self.commentObjectList = []
#         self.viewCount = 0
#         self.price = 0
#         self.currency = ""
#         self.favoriteCounter = 0
#         self.sellCounter = 0
#         self.sellVideoId = ""
#         self.trailerId = ""
#         self.videoType = ""
#         self.fileName = ""
#         self.discountValue = 0
#
####################################################################################

class User:
    def __init__(self):
        self.username = ""
        self.password = ""
        self.email = ""
        self.favoriteList = []
        self.historyList = []
        self.loginStampList = []
        self.ipLoginList = []
        self.videoList = []
        self.id = ""
        self.nickName = ""
        self.role = ""
        self.cardList = []
        self.purchasedVideosList = []
        self.followerList = []
        self.followingList = []
        self.unreadConversationsList = []


################################## H E L P E R ####################################
#        
# class NewUserObject:
#     def __init__(self):
#         self.username = ""
#         self.password = ""
#         self.email = ""
#         self.favoriteList = []
#         self.historyList = []
#         self.loginStampList = []
#         self.ipLoginList = []
#         self.videoList = []
#         self.id = ""
#         self.nickName = ""
#         self.role = ""
#         self.cardList = []
#         self.purchasedVideosList = []
#         self.followerList = []
#         self.followingList = []
#         self.unreadConversationsList = []
#         self.verified
#
####################################################################################


class UserPageData:
    def __init__(self):
        self.userName = ""
        self.userId = ""
        self.id = ""
        self.nickName = ""
        self.userDiscription = ""
        self.profilePicturePath = ""
        self.picturePathList = []
        self.videoList = []
        self.commentList = []
        self.catchPhrase = ""
        self.categorieList = []
        
class CategoryAnalyticsObject:
    def __init__(self):
        self.id = ""
        self.categorieId = ""
        self.name = ""
        self.counter = 0
        self.lastUpdate = ""
        self.createdOn = "" 
        self.searchTermCharts = CategoryAnalyticsObject.SearchTermChartList()
        
    class SearchTermChartList():
        def __init__(self):
            self.searchTerm = ""
            self.Counter = ""
            self.lastUpdate = ""
            self.createdOn = "" 
            self.id = ""
            
class PornStarAnalyticsObject:
    def __init__(self):
        self.id = ""
        self.name = ""
        self.tagList = ""
        self.videoList = []
        self.bio = ""
        self.data = ""
        self.counter = 0
        self.lastUpdate = ""
        self.createdOn = "" 
        self.searchTermCharts = PornStarAnalyticsObject.SearchTermChartList()
        
    class SearchTermChartList():
        def __init__(self):
            self.searchTerm = ""
            self.Counter = ""
            self.lastUpdate = ""
            self.createdOn = "" 
            self.id = ""
        
class AnaltycisObject:
    def __init__(self):
        self.metaInformationObject = MetaInformationObject()
        self.watchCounter = 0
        self.upVotes = 0
        self.downVotes = 0
        self.lastUpdate = ""
        self.createdOn = "" 
        self.id = ""
        
class ErrorMessage:
    def __init__(self, _title, _content):
        self.title = _title
        self.content = _content
        
class Conversation:
    def __init__(self):
        self.starterId = ""
        self.participentId = ""
        self.senderUserName = ""
        self.participentUsername = ""
        self.participentNickName = ""
        self.messageList = []
        self.id = ""
        self.read = False
        
class Message:
    def __init__(self):
        self.senderId = ""
        self.receiverId = ""
        self.senderUserName = ""
        self.receiverUserName = ""
        self.titleText = ""
        self.messageText = ""
        self.timeStamp = ""
        self.senderNickName = ""
        self.id = ""
        self.conversationId = ""
        self.offer = ""
        self.read = False
#       self.link = ""
        
    def CreateMessage(_senderId, _receiverId, _senderUserName, _receiverUserName, _titleText, _messageText, _timeStamp, _senderNickName):
        message = Message()
        message.senderId = _senderId
        message.receiverId = _receiverId
        message.senderUserName = _senderUserName
        message.receiverUserName = _receiverUserName
        message.titleText = _titleText
        message.messageText = _messageText
        message.timeStamp = _timeStamp
        message.senderNickName = _senderNickName
        return message     
    
class CustomSale:
    def __init__(self):
        self.id = ""
        self.sellerId = ""
        self.buyerId = ""
        self.timeStamp = ""
        self.offerTitle = ""
        self.offerText = ""
        self.status = ""
        self.offerPrice = ""
        
class Tag():
    def __init__(self, _name):
        self.name = _name
        self.counter = 0