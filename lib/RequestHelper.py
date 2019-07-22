import requests
import simplejson as json
import pprint

# BUILD BODY DATA FROM JSON
def getBodyData(bodyParameters):
    bodyData = {}
    for parameter in json.loads(str(bodyParameters).replace("\'", "\"")): 
        for key in parameter:
            bodyData[key] = parameter[key]
    return bodyData

# BUILD HEADER DATA FROM JSON
def getHeaderData(headerParameters):
    headerData = {}
    for parameter in json.loads(str(headerParameters).replace("\'", "\"")): 
        for key in parameter:
            headerData[key] = parameter[key]
    return headerData

def buildPostRequest(url, bodyParameters, headerParameters):
    if (url is None):
        return None
    elif (headerParameters is not None and bodyParameters is not None):
        bodyData = getBodyData(bodyParameters)
        headerData = getHeaderData(headerParameters)
        return requests.post(url, data=bodyData, headers=headerData)
    elif (bodyParameters is not None):
        bodyData = getBodyData(bodyParameters)
        return requests.post(url, data=bodyData)
    elif (headerParameters is not None):
        headerData = getHeaderData(headerParameters)
        return requests.post(url, data={}, headers=headerData)
    else:
        return None

def buildGetRequest(url, bodyParameters, headerParameters):
    if (url is None):
        return None
    elif (headerParameters is not None and bodyParameters is not None):
        bodyData = getBodyData(bodyParameters)
        headerData = getHeaderData(headerParameters)
        return requests.get(url, data=bodyData, headers=headerData)
    elif (bodyParameters is not None):
        bodyData = getBodyData(bodyParameters)
        return requests.get(url, data=bodyData)
    elif (headerParameters is not None):
        headerData = getHeaderData(headerParameters)
        return requests.get(url, data={}, headers=headerData)
    else:
        return None