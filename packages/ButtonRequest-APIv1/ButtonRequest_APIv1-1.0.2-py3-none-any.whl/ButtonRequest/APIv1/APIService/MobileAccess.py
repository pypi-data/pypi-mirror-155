import requests
from ..CommonFunction.FilterData import FilterData


class MobileAccess:
    def __init__(self, apiToken, apiServer):
        self.apiToken = apiToken
        self.apiServer = apiServer
        self.filterData = FilterData()

    def fetch(self, filterDict=[]):
        try:
            resp = requests.post(self.apiServer + "/mobileDevice/fetch", verify=False, headers={
                "Authorization": "Bearer " + self.apiToken,
                "Accept": "application/json"
            })
            json_res=resp.json()
            return {"result": json_res["result"], "data": self.filterData.fetchMobileAccessToken(data=json_res["data"], filterDict=filterDict)}
        except:
            return {"result": "error","data": []}


    def new(self, nickname):
        try:
            resp = requests.post(self.apiServer + "/mobileDevice/new/"+nickname, verify=False, headers={
                "Authorization": "Bearer " + self.apiToken,
                "Accept": "application/json"
            })
            return resp.json()
        except:
            return {"result": "error","data": []}

    def amendNickname(self, case_id, newNickname):
        try:
            resp = requests.post(self.apiServer + "/mobileDevice/amend/"+case_id+"?nickname="+newNickname, verify=False, headers={
                "Authorization": "Bearer " + self.apiToken,
                "Accept": "application/json"
            })
            return resp.json()
        except:
            return {"result": "error","data": []}

    def revoke(self, case_id):
        try:
            resp = requests.post(self.apiServer + "/mobileDevice/revoke/"+ case_id, verify=False, headers={
                "Authorization": "Bearer " + self.apiToken,
                "Accept": "application/json"
            })
            return resp.json()
        except:
            return {"result": "error","data": []}