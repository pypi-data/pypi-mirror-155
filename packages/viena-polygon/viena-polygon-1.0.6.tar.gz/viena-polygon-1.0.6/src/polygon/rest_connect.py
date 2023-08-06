import json
import os

import requests

DATASET_LIST_URI = "/images/account/{accountId}/datasets"
DATASET_DELETE_URI = ""
DATASET_DETAILS_URI = ""
DATASET_CREATE_URI = ""
DATASET_MERGE_URI = ""

serverUrl="http://ec2co-ecsel-120oaoc0msxmg-363566620.us-east-1.elb.amazonaws.com:8081/"
#serverUrl="http://localhost:8081/"

def generate_access_token_from_config_file():
    pass

def generate_access_token_from_apikey():
    if (not os.path.isfile(os.path.expanduser('~/.polygon/credentials'))):
        return "Not Found"
    f = open(os.path.expanduser('~/.polygon/credentials'), "r")
    token = f.read()
    if (token == ""):
        return "Not Found"
    token = token.split(":")
    API_KEY = token[1] 
    tokenUrl = serverUrl + "admin/validate/apikey/" + API_KEY
    response = requests.get(tokenUrl)
    return response.json()


def dataset_list():
    #TODO for now just get accountid from apikey??? or some other way
    accces_token = generate_access_token_from_apikey()
    if (accces_token == "Not Found" or accces_token == "Not Found"):
        return "API KEY not Found, Please run 'polygon --configure' to configure"
    accountId=accces_token["accountId"]
    accessType=accces_token["accessList"]
    if not 'read' in accessType:
        return "API does not have the read access"
    if(accountId==None):
        return "Invalid API key"
    auth_headers = {'Authorization': 'Bearer '+accountId}
    url=serverUrl+"images/account/"+accountId+"/datasets"
    response = requests.get(url, headers=auth_headers)
    return response.json()

def createDataset(name, classname, clodustoragename):
    accces_token = generate_access_token_from_apikey()
    if (accces_token == "Not Found" or accces_token == "Not Found"):
        return "API KEY not Found, Please run 'polygon --configure' to configure"
    accountId = accces_token["accountId"]
    accessType = accces_token["accessList"]
    if not 'write' in accessType:
        return "API does not have the read access"
    if (accountId == None):
        return "Invalid API key"
    if (name !=None and clodustoragename !=None):
        print("Started creating the dataset")
        auth_headers = {'Authorization': 'Bearer ' + accountId}
        data = {'datasetName': name, 'cloudStorageName': clodustoragename, 'objectList': classname,'accountId':accountId}
        headers = {'Content-Type': 'application/json'}

        url = serverUrl + "/dataset/createfromcontainer"
        response = requests.post(url, headers={"content-type": "application/json"}, data=json.dumps(data))
        if (response.status_code == 200):
            response = "Successfully created the dataset"
        else:
            response = "Create dataset failed"
        return response

def dataset_merge(dataset_id_list, dataset_name_list,name):
    accces_token = generate_access_token_from_apikey()
    if (accces_token == "Not Found" or accces_token == "Not Found"):
        return "API KEY not Found, Please run 'polygon --configure' to configure"
    accountId = accces_token["accountId"]
    accessType = accces_token["accessList"]
    if not 'write' in accessType:
        return "API does not have the read access"
    if (accountId == None):
        return "Invalid API key"
    if(len(dataset_id_list) >0):
        print("Started merging the datasets")
        auth_headers = {'Authorization': 'Bearer '+accountId}
        data = {'datasetIdsTobeMerged': dataset_id_list,'newDatasetName':name,'accountId':accountId}
        headers = {'Content-Type': 'application/json'}

        url = serverUrl + "dataset/mergedatasets"
        response = requests.post(url, headers={"content-type":"application/json"}, data=json.dumps(data))
        if(response.status_code==200):
            response="Successfully merged the datasets"
        else:
            response="Merging failed"
        return response
    if (len(dataset_name_list) > 0):
        print("Started merging the datasets")
        auth_headers = {'Authorization': 'Bearer ' + accountId}
        data = {'datasetNamesTobeMerged': dataset_name_list, 'newDatasetName': name, 'accountId': accountId}
        headers = {'Content-Type': 'application/json'}

        url = serverUrl + "dataset/cli/mergedatasetsbyname"
        response = requests.post(url, headers={"content-type": "application/json"}, data=json.dumps(data))
        if (response.status_code == 200):
            response = "Successfully merged the datasets"
        else:
            response = "Merging failed"
        return response

def dataset_details(dataset_name,dataset_id):
    accces_token = generate_access_token_from_apikey()
    if (accces_token == "Not Found" or accces_token == "Not Found"):
        return "API KEY not Found, Please run 'polygon --configure' to configure"
    accountId = accces_token["accountId"]
    accessType = accces_token["accessList"]
    if not 'read' in accessType:
        return "API does not have the read access"
    if (accountId == None):
        return "Invalid API key"
    if dataset_id != "None":
        auth_headers = {'Authorization': 'Bearer '+accountId}
        url=serverUrl+"dataset/cli/account/"+accountId+"/"+dataset_id
        response = requests.get(url, headers=auth_headers)
        return response.json()
    elif dataset_name != "None":
        auth_headers = {'Authorization': 'Bearer '+accountId}
        data = {'name': dataset_name}
        url = serverUrl + "dataset/cli/account/" + accountId
        response = requests.get(url, headers={'Content-Type': 'application/json' }, json=data)
        return response.json()

def dataset_delete(dataset_name,dataset_id):
    accces_token = generate_access_token_from_apikey()
    if (accces_token == "Not Found" or accces_token == "Not Found"):
        return "API KEY not Found, Please run 'polygon --configure' to configure"
    accountId = accces_token["accountId"]
    accessType = accces_token["accessList"]
    if not 'read' in accessType:
        return "API does not have the read access"
    if (accountId == None):
        return "Invalid API key"
    if dataset_id != "None":
        auth_headers = {'Authorization': 'Bearer '+accountId}
        data = {'datasetId': dataset_id, 'accountId': accountId}
        url = serverUrl + "dataset/cli/account/" + accountId+"/dataset/"+dataset_id+"/delete"
        response = requests.post(url, params=data)
        return response.text
    elif dataset_name != "None":
        auth_headers = {'Authorization': 'Bearer '+accountId}
        data = {'datasetname': dataset_name, 'accountId': accountId}
        url = serverUrl + "dataset/cli/account/" + accountId + "/deletedatasetbyname"
        response = requests.post(url, params=data)
        return response.text

def search_details(phrase,parsedSql):
    accces_token = generate_access_token_from_apikey()
    if (accces_token == "Not Found" or accces_token == "Not Found"):
        return "API KEY not Found, Please run 'polygon --configure' to configure"
    accountId = accces_token["accountId"]
    accessType = accces_token["accessList"]
    if not 'read' in accessType:
        return "API does not have the read access"
    if (accountId == None):
        return "Invalid API key"
    if(phrase!="None"):
        auth_headers = {'Authorization': 'Bearer ' + accountId}
        data = {'queryphrase': phrase,'accountId':accountId,'pagenum':1}
        url = serverUrl + "search/images/1/account/"+accountId
        response = requests.post(url, params=data)
        return response.json()
    if (parsedSql != "None"):
        y = json.loads(parsedSql)
        searchRequestBody={
            "searchFilterMap": {
                "status": [],
                "dataset": []
            },
            "tagsList": []
        }
        auth_headers = {'Authorization': 'Bearer ' + accountId}
        data = {'queryphrase': y["classname"], 'accountId': accountId, 'pagenum': 1}
        url = serverUrl + "search/images/1/account/" + accountId
        response = requests.post(url, params=data,json=searchRequestBody)
        return response.json()

def containerList():
    accces_token = generate_access_token_from_apikey()
    if (accces_token == "Not Found" or accces_token == "Not Found"):
        return "API KEY not Found, Please run 'polygon --configure' to configure"
    accountId = accces_token["accountId"]
    accessType = accces_token["accessList"]
    if not 'read' in accessType:
        return "API does not have the read access"
    if (accountId == None):
        return "Invalid API key"
    auth_headers = {'Authorization': 'Bearer ' + accountId}
    url = serverUrl + "cloudstorage/account/"+accountId+"/cloudlist"
    response = requests.get(url, headers=auth_headers)
    return response.json()

def createContainer(cloudstoragename,cloudtype,authentication,containername,bucketname,
            accontname,accesskey,secretid,sastoken,manifestjson,region):
    accces_token = generate_access_token_from_apikey()
    if (accces_token == "Not Found" or accces_token == "Not Found"):
        return "API KEY not Found, Please run 'polygon --configure' to configure"
    accountId = accces_token["accountId"]
    accessType = accces_token["accessList"]
    if not 'read' in accessType:
        return "API does not have the read access"
    if (accountId == None):
        return "Invalid API key"
    auth_headers = {'Authorization': 'Bearer ' + accountId}
    url = serverUrl + "cloudstorage/registercloud"

    if (cloudtype == "aws_s3" and authentication == "account_authentication"):
        data = { 'displayName': cloudstoragename,'provider': cloudtype,'containerName': bucketname,'authorizationType': authentication,
                'accesskey': accesskey,'secretkey': secretid,'region': region,'cloudAccountName': accontname,'sasToken': sastoken,
                'accountId': accountId,
                'jsonFileNmae': manifestjson,
                'status': 1}
        response = requests.post(url, headers={"content-type": "application/json"}, data=json.dumps(data))
        return response.text
    if (cloudtype == "aws_s3" and authentication == "annonymous_access"):
        data = {'displayName': cloudstoragename,
                'provider': cloudtype,
                'containerName': bucketname,
                'authorizationType': authentication,
                'accesskey': accesskey,
                'secretkey': secretid,
                'region': region,
                'cloudAccountName': accontname,
                'sasToken': sastoken,
                'accountId': accountId,
                'jsonFileNmae': manifestjson,
                'status': 1
                }
        response = requests.post(url, headers={"content-type": "application/json"}, data=json.dumps(data))
        return response.text
    if (cloudtype == "azure_container" and authentication == "account_authentication"):
        data = {'displayName': cloudstoragename,
                'provider': cloudtype,
                'containerName': containername,
                'authorizationType': authentication,
                'accesskey': accesskey,
                'secretkey': secretid,
                'region': region,
                'cloudAccountName': accontname,
                'sasToken': sastoken,
                'accountId': accountId,
                'jsonFileNmae': manifestjson,
                'status': 1
                }
        response = requests.post(url, headers={"content-type": "application/json"}, data=json.dumps(data))
        return response.text
    if (cloudtype == "azure_container" and authentication == "annonymous_access"):
        data = {'displayName': cloudstoragename,
                'provider': cloudtype,
                'containerName': containername,
                'authorizationType': authentication,
                'accesskey': accesskey,
                'secretkey': secretid,
                'region': region,
                'cloudAccountName': accontname,
                'sasToken': sastoken,
                'accountId': accountId,
                'jsonFileNmae': manifestjson,
                'status': 1
                }
        response = requests.post(url, headers={"content-type": "application/json"}, data=json.dumps(data))
        return response.text

def container_details(cloudstoragename,cloudstorageid):
    accces_token = generate_access_token_from_apikey()
    if (accces_token == "Not Found" or accces_token == "Not Found"):
        return "API KEY not Found, Please run 'polygon --configure' to configure"
    accountId = accces_token["accountId"]
    accessType = accces_token["accessList"]
    if not 'read' in accessType:
        return "API does not have the read access"
    if (accountId == None):
        return "Invalid API key"
    if cloudstorageid != "None":
        auth_headers = {'Authorization': 'Bearer '+accountId}
        url=serverUrl+"cloudstorage/account/"+accountId+"/cloudstoragedetailsbyid/"+cloudstorageid
        response = requests.get(url, headers=auth_headers)
        return json.dumps(response.json(), indent=3)
    elif cloudstoragename != "None":
        auth_headers = {'Authorization': 'Bearer '+accountId}
        data = {'storagename': cloudstoragename}
        url=serverUrl+"cloudstorage/account/"+accountId+"/cloudstoragedetailsbyname"
        response = requests.get(url,params=data)
        return response.text

def delete_container(cloudstorage_name,cloudstorage_id):
    accces_token = generate_access_token_from_apikey()
    if (accces_token == "Not Found" or accces_token == "Not Found"):
        return "API KEY not Found, Please run 'polygon --configure' to configure"
    accountId = accces_token["accountId"]
    accessType = accces_token["accessList"]
    if not 'read' in accessType:
        return "API does not have the read access"
    if (accountId == None):
        return "Invalid API key"
    if cloudstorage_id != "None":
        auth_headers = {'Authorization': 'Bearer '+accountId}
        data = {'datasetId': cloudstorage_id, 'accountId': accountId}
        url = serverUrl + "cloudstorage/account/" + accountId+"/cloudstorage/"+cloudstorage_id+"/delete"
        response = requests.post(url, params=data)
        return response.text
    elif cloudstorage_name != "None":
        auth_headers = {'Authorization': 'Bearer '+accountId}
        data = {'datasetname': cloudstorage_name, 'accountId': accountId}
        url = serverUrl + "cloudstorage/account/" + accountId + "/cloudstorage/deletecloudstoragebyname"
        response = requests.post(url, params=data)
        return response.text

