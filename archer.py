import requests
import json
import logging
import os
import datetime

class archer:
    def __init__(self):
        if not os.path.exists("Logs"):
            os.makedirs("Logs")
        currentDate = datetime.datetime.now().strftime("%Y-%m-%d")
        logFileName = os.path.join("Logs",f"ArcherServiceNowIntegration.Archer.{currentDate}.log")
        self.logger = logging.getLogger(__name__)
        archerHandler = logging.FileHandler(logFileName)
        archerHandler.setLevel(logging.DEBUG)
        archerHandler.setFormatter(logging.Formatter("%(asctime)s - [%(levelname)s] - %(message)s"))
        self.logger.addHandler(archerHandler)
        with open('config.json','r')as f:
            config = json.load(f)
        self.url = config['archer']['url']
        self.username = config['archer']['username']
        self.password = config['archer']['password']
        self.instance = config['archer']['instance']
        self.domain = config['archer']['domain']
        self.sessionToken = ""
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
        if(response.status_code == 200):
            resp = response.json()
            if(resp['IsSuccessful'] == True):
                self.sessionToken = response.json()['RequestedObject']['SessionToken']
                self.logger.info(f"Archer API Login successful")
            else:
                self.logger.error(f"Archer API Login failed : {response.json()}")
        else:
            self.logger.critical(f"Archer API Login failed : {response.json()}")

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
        self.logger1.info('Archer Create Record responce status code - '+ response.status_code)
        if(response.status_code == 200):
            resp = response.json()
            self.logger.info('Archer record created with Id - '+resp['RequestedObject']['Id'])
            return resp['RequestedObject']['Id']
        else:
            self.logger.error('Archer record creation failed - '+response.json())
            return None


        
        