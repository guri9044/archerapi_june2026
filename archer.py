import requests
import json
import logging
import os
import datetime
import xmltodict

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
        self.Records = []
        self.headers = {
            "Authorization": "Archer session-id=\"" + self.sessionToken + "\"",
            "Content-Type": "application/json"
        }
        self.soapHeaders = {
            'Content-Type': 'application/x-www-form-urlencoded'
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
        self.logger.info(f"Archer Create Record responce status code - {str(response.status_code)}")
        if(response.status_code == 200):
            resp = response.json()
            self.logger.info(f"Archer record created with Id - {resp['RequestedObject']['Id']}")
            return resp['RequestedObject']['Id']
        else:
            self.logger.error(f"Archer record creation failed - {response.json()}")
            return None
    
    def updateRecords(self,data):
        url = f"{self.url}/platformapi/core/content"
        payload = json.dumps(data)
        response = requests.put(url, headers=self.headers, data=payload)
        self.logger.info(f"Archer Update Record responce status code - {str(response.status_code)}")
        if(response.status_code == 200):
            resp = response.json()
            self.logger.info(f"Archer record updated with Id - {resp['RequestedObject']['Id']}")
            return resp['RequestedObject']['Id']
        else:
            self.logger.error(f"Archer record update failed - {response.json()}")
            return None
    
    def getRecordsfromReport(self,reportIdOrGuid, pageNumber = 1):
        url = f"{self.url}/ws/search.asmx/SearchRecordsByReport"
        payload = f'sessionToken={self.sessionToken}&reportIdOrGuid={reportIdOrGuid}&pageNumber={pageNumber}'
        response = requests.request("POST", url, headers=self.soapHeaders, data=payload)
        response = response.text
        data_dict = xmltodict.parse(response)
        jsonData = json.loads(json.dumps(data_dict))
        recordXML = jsonData["string"]["#text"]
        recordxmldict = xmltodict.parse(recordXML)
        totalRecord = int(recordxmldict['Records']['@count'])
        currentReportRecord = len(recordxmldict['Records']['Record'])
        iterations = totalRecord // currentReportRecord
        if(iterations > 0 and totalRecord % currentReportRecord != 0):
            iterations+=1
        parentRec = recordxmldict['Records']['Record']
        for rec in parentRec:
            if rec['Record']:
                childrec = rec['Record']
                fields = childrec['Field']
                if(isinstance(fields, list)):
                    for field in fields:
                        rec['Field'].append(field)
                else:
                    rec['Field'].append(fields)

        self.Records = parentRec
        print("Iterations : ",iterations)
        if(iterations>1):
            for i in range(2,iterations+1):
                print(i)
                url = f"{self.url}/ws/search.asmx/SearchRecordsByReport"
                payload = f'sessionToken={self.sessionToken}&reportIdOrGuid={reportIdOrGuid}&pageNumber={i}'
                response = requests.request("POST", url, headers=self.soapHeaders, data=payload)
                response = response.text
                data_dict = xmltodict.parse(response)
                jsonData = json.loads(json.dumps(data_dict))
                recordXML = jsonData["string"]["#text"]
                recordxmldict = xmltodict.parse(recordXML)
                parentRec = recordxmldict['Records']['Record']
                for rec in parentRec:
                    if rec['Record']:
                        childrec = rec['Record']
                        fields = childrec['Field']
                        if(isinstance(fields, list)):
                            for field in fields:
                                rec['Field'].append(field)
                        else:
                            rec['Field'].append(fields)
                self.Records.extend(parentRec)
        with open("archerRecords.json","w") as f:
            json.dump(self.Records,f)
        return self.Records
    
        
            
        