import requests
import json
import requests
import base64

class snow:
    def __init__(self):
        with open('config.json','r')as f:
            config = json.load(f)
        self.url = config['servicenow']['url']
        self.username = config['servicenow']['username']
        self.password = config['servicenow']['password']
        self.authType = config['servicenow']['authType']
        self.oauth_Token = config['servicenow']['oauth_Token']
        basicAuthString = self.username + ":" + self.password
        base64Auth = base64.b64encode(basicAuthString.encode()).decode()
        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization" : "Basic "+base64Auth
        }

    def getRecords(self,table,query,fields):
        url = f"{self.url}/api/now/table/{table}"
        if query and fields:
            url = url+"?sysparam_query="+query+"&sysparam_fields="+fields
        elif query:
            url = url+"?sysparam_query="+query
        elif fields:
            url = url+"?sysparm_fields="+fields
        print("URL : ",url)
        response = requests.get(url,headers=self.headers)
        return response.json()['result']
        
    def getRecord(self,table,id):
        url = self.url + "/api/now/table/"+table+""+id
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        response = requests.get(url, headers=headers)
        return response.json()
    
    def createRecord(self,table,record):
        print(self.url)

    def updateRecord(self,table,id,record):
        url = f"{self.url}/api/now/table/{table}/{id}"
        response = requests.patch(url, headers=self.headers, data=json.dumps(record))
        return response.json()

    def deleteRecord(self,table,id):
        print(self.url)