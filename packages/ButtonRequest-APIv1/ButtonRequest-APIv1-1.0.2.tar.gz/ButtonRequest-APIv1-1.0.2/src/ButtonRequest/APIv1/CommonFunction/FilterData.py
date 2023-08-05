




class FilterData:
    ##[
    ##    "msg_id"=>""
    ##    "device_id"=>""
    ##    "pin"=>""
    ##    "shared_to_me"=>""
    ##]

    def fetchMessages(self, data, filterDict):
        adjustedFilterDict=self.trimDictByKey(filterDict, ["msg_id","device_id","pin","shared_to_me"])
        return self.filterArrayByEquality(data, adjustedFilterDict)
    
    def fetchDeviceList(self, data, filterDict):
        adjustedFilterDict=self.trimDictByKey(filterDict, ["status","repeated_message"])
        return self.filterArrayByEquality(data, adjustedFilterDict)
    
    def fetchMobileAccessToken(self, data, filterDict):
        adjustedFilterDict=self.trimDictByKey(filterDict, ["case_id","deleted_from_phone"])
        return self.filterArrayByEquality(data, adjustedFilterDict)
    
    def fetchDeviceSharedToMe(self, data, filterDict):
        adjustedFilterDict=self.trimDictByKey(filterDict, ["case_id","device_id", "owner_email", "right"])
        return self.filterArrayByEquality(data, adjustedFilterDict)
    
    def trimDictByKey(self, dict0, keyAllowedArray):
        dict1={}
        for key in dict0:
            if key in keyAllowedArray:
                dict1[key]=dict0[key]
        return dict1

    def filterArrayByEquality(self, array, conditionDict):
        newArray=[]
        if len(conditionDict)>0:
            for item in array:
                add=True
                for key in conditionDict:
                    if item[key] != conditionDict[key] :
                        add = False

                if add:
                    newArray.append(item)
           
        else:
            newArray=array
        
        return newArray
    