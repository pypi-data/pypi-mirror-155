from .APIService.Message import Message
from .APIService.MobileAccess import MobileAccess
from .APIService.DeviceList import DeviceList
from .APIService.DShare import DeviceShare


class Client:
    def __init__(self, apiToken):
        self.apiToken = apiToken
        self.apiServer = "https://button-request.herokuapp.com/api/v1"
        self.message = Message(self.apiToken, self.apiServer)
        self.mobileAccess = MobileAccess(self.apiToken, self.apiServer)
        self.deviceList = DeviceList(self.apiToken, self.apiServer)
        self.deviceShare = DeviceShare(self.apiToken, self.apiServer)


