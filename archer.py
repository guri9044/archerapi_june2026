from oDataCreate import url
import requests
import json

class archer:
    def __init__(self):
        with open('config.json','r')as f:
            config = json.load(f)
        self.url = config['archer']['url']
        self.username = config['archer']['username']
        self.password = config['archer']['password']
        self.instance = config['archer']['instance']
        self.domain = config['archer']['domain']
        self.login()
        self.headers = {
            "Authorization": "Archer session-id=\"" + self.sessionToken + "\"",
            "Content-Type": "application/json"
        }
    
    def login(self):
        url =  f"{self.url}/platformapi/core/security/login"
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        payload = {
            "InstanceName":self.instance,
            "Username":self.username,
            "UserDomain":self.domain,
            "Password":self.password
        }
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        self.sessionToken = response.json()['RequestedObject']['SessionToken']

    def csrfToken(self):
        url = self.url + "/api/V2/internal/LookUp?node=root"
        headers = {"Cookie": "__ArcherSessionCookie__=" + self.sessionToken}
        response = requests.get(url, headers=headers)
        headers_dict = dict(response.headers)
        if 'csrf-token' in headers_dict:
            self.csrf_token = headers_dict['csrf-token']
            self.headers['x-csrf-token'] = self.csrf_token

    class recordBuilder:
        def __init__(self,levelID):
            self.record = {"Content": {"LevelId":levelID,"FieldContents":{}}}
        def addField(self,fieldID,type,value):
            self.record['Content']['FieldContents'][fieldID] = {"Type":type,"Value":value,"FieldId":fieldID}
        def getJSON(self):
            return self.record
            
    def createRecords(self,data):
        url = f"{self.url}/platformapi/core/content"
        payload = json.dumps(data)
        response = requests.post(url, headers=self.headers, data=payload)
        resp = response.json()
        return resp['RequestedObject']['Id']

        
        