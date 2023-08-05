import jsons

import requests
import urllib.parse
from ..CommonFunction.FilterData import FilterData


class DeviceList:
    def __init__(self, apiToken, apiServer):
        self.apiToken = apiToken
        self.apiServer = apiServer
        self.filterData = FilterData()

    def fetch(self, device_id="", filterDict=[]):
        try:
            resp = requests.post(self.apiServer + "/buttonDevice/myDevice/list/" + device_id, verify=False, headers={
                "Authorization": "Bearer " + self.apiToken,
                "Accept": "application/json"
            })
            json_res = resp.json()
            return {"result": json_res["result"], "data": self.filterData.fetchDeviceList(data=json_res["data"], filterDict = filterDict)}
        except:
            return {"result": "error","data": []}

    def repeatedMessage(self, device_id, action):
        try:
            resp = requests.post(self.apiServer + '/buttonDevice/myDevice/repeatedMessage/'+device_id+'/'+action, verify=False, headers={
                "Authorization": "Bearer " + self.apiToken,
                "Accept": "application/json"
            })
            return resp.json()
        except:
            return {"result": "error","data": []}

    def buttonMessageUpdate(self, device_id, buttonMessageArray):
        try:
            passData = {
                "dataArray": buttonMessageArray
            }
            url = self.apiServer + "/buttonDevice/myDevice/buttonMessageUpdate/updateOrNew/" + device_id
            payload ='passData='+urllib.parse.quote(jsons.dumps(passData))
            headers = {
                'Authorization': 'Bearer '+self.apiToken,
                'Content-Type': 'application/x-www-form-urlencoded'
            }
            response = requests.post(url, headers=headers, data=payload, verify=False)

            return response.json()
        except:
            return {"result": "error","data": []}

    def buttonMessageDelete(self, device_id, buttonIdArray):
        try:
            passData = {
                "dataArray": buttonIdArray
            }
            url = self.apiServer + "/buttonDevice/myDevice/buttonMessageUpdate/delete/" + device_id
            payload ='passData='+urllib.parse.quote(jsons.dumps(passData))
            headers = {
                'Authorization': 'Bearer '+self.apiToken,
                'Content-Type': 'application/x-www-form-urlencoded'
            }
            response = requests.post( url, headers=headers, data=payload, verify=False)

            return response.json()
        except:
            return {"result": "error","data": []}

    def newDevice(self, nickname):
        try:
            url = self.apiServer + "/buttonDevice/myDevice/new/" + nickname
            headers = {
                'Authorization': 'Bearer '+self.apiToken,
                'Content-Type': 'application/json'
            }
            response = requests.post( url, headers=headers,  verify=False)
            return response.json()
        except:
            return {"result": "error","data": []}