import requests
from ..CommonFunction.FilterData import FilterData


class DeviceShare:
    def __init__(self, apiToken, apiServer):
        self.apiToken = apiToken
        self.apiServer = apiServer
        self.filterData = FilterData()

    def toMeFetch(self, filterDict=[]):
        try:
            resp = requests.post(self.apiServer + '/buttonDevice/deviceSharedToMe/fetch', verify=False, headers={
                "Authorization": "Bearer " + self.apiToken,
                "Accept": "application/json"
            })
            json_res=resp.json()
            return {"result": json_res["result"], "data": self.filterData.fetchDeviceSharedToMe(data=json_res["data"], filterDict=filterDict)}
        except:
            return {"result": "error","data": []}

    def giveUpShareeRight(self, case_id):
        try:
            resp = requests.post(self.apiServer + '/buttonDevice/deviceSharedToMe/delete/'+case_id, verify=False, headers={
                "Authorization": "Bearer " + self.apiToken,
                "Accept": "application/json"
            })
            return resp.json()
        except:
            return {"result": "error","data": []}

    def shareTo(self, device_id, email):
        try:
            resp = requests.post(self.apiServer + '/buttonDevice/shareDevice/new/'+email+'/'+device_id, verify=False, headers={
                "Authorization": "Bearer " + self.apiToken,
                "Accept": "application/json"
            })
            return resp.json()
        except:
            return {"result": "error","data": []}

    def changeShareeRight(self, case_id, right):
        try:
            resp = requests.post(self.apiServer + '/buttonDevice/shareDevice/changeRight/'+case_id+'/'+right
                                              , verify=False, headers={
                "Authorization": "Bearer " + self.apiToken,
                "Accept": "application/json"
            })
            return resp.json()
        except:
            return {"result": "error","data": []}
