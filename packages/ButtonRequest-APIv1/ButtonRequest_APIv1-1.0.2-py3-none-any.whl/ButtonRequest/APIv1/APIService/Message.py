import requests
from ..CommonFunction.FilterData import FilterData


class Message:
    def __init__(self, apiToken, apiServer):
        self.apiToken = apiToken
        self.apiServer = apiServer
        self.filterData = FilterData()

    def fetch(self, filterDict=[]):
        try:
            resp = requests.post(self.apiServer + '/message/fetch', verify=False, headers={
                "Authorization": "Bearer " + self.apiToken,
                "Accept": "application/json"
            })
            json_res = resp.json()
            return {"result": json_res["result"],"data": self.filterData.fetchMessages(data=json_res["data"], filterDict=filterDict)}
        except:
            return {"result": "error","data": []}

    def delete(self, msg_id):
        try:
            resp = requests.post(self.apiServer + "/message/delete/" + msg_id, verify=False, headers={
                "Authorization": "Bearer " + self.apiToken,
                "Accept": "application/json"
            })
            return resp.json()
        except:
            return {"result": "error","data": []}

    def pinStatus(self, messageId, pinUnpin):
        try:
            resp = requests.post(self.apiServer + "/message/pinStatus/" + messageId + "/" + pinUnpin, verify=False,
                                     headers={
                                         "Authorization": "Bearer " + self.apiToken,
                                         "Accept": "application/json"
                                     }
                                 )
            return resp.json()
        except:
            return {"result": "error","data": []}
