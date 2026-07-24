import requests
import json
import requests
import base64
import logging
import os
import datetime

class snow:
    def __init__(self):
        if not os.path.exists("Logs"):
            os.makedirs("Logs")
        currentDate = datetime.datetime.now().strftime("%Y-%m-%d")
        fileName = os.path.join("Logs",f"ArcherServiceNowIntegration.ServiceNow.{currentDate}.log")
        self.logger = logging.getLogger(__name__)
        snowHandler = logging.FileHandler(fileName)
        snowHandler.setLevel(logging.DEBUG)
        snowHandler.setFormatter(logging.Formatter("%(asctime)s - [%(levelname)s] - %(message)s"))
        self.logger.addHandler(snowHandler)
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
            url = url+"?sysparm_query="+query+"&sysparm_fields="+fields
        elif query:
            url = url+"?sysparm_query="+query
        elif fields:
            url = url+"?sysparm_fields="+fields
        print("URL : ",url)
        response = requests.get(url, headers=self.headers)
        if(response.status_code == 200):
            recordArray = self._parseJSON(response)['result']
            self.logger.info(f"Successfully retrieved {len(recordArray)} records from {table}")
            return recordArray
        else:
            self.logger.error(f"Failed to retrieve records from {table} : {response.status_code}")
            return None

    def _parseJSON(self, response):
        try:
            return response.json()
        except ValueError:
            if 'Instance Hibernating' in response.text:
                self.logger.error("ServiceNow instance is hibernating - wake it at developer.servicenow.com")
                raise RuntimeError("ServiceNow instance is hibernating; wake it at developer.servicenow.com and retry.")
            self.logger.error(f"Non-JSON response from ServiceNow (HTTP {response.status_code}): {response.text[:200]}")
            raise RuntimeError(f"Non-JSON response from ServiceNow (HTTP {response.status_code}); check URL/credentials in config.json.")
        
    def getRecord(self,table,id):
        url = self.url + "/api/now/table/"+table+""+id
        response = requests.get(url, headers=self.headers)
        return response.json()
    
    def createRecord(self,table,record):
        url = f"{self.url}/api/now/table/{table}"
        response = requests.post(url, headers=self.headers, data=json.dumps(record))
        rec = self._parseJSON(response)
        return rec["result"]["sys_id"]

    def updateRecord(self,table,id,record):
        url = f"{self.url}/api/now/table/{table}/{id}"
        response = requests.patch(url, headers=self.headers, data=json.dumps(record))
        rec = self._parseJSON(response)
        return rec["result"]["sys_id"]

    def getUserByUserID(self,userid,emailId):
        url = f"{self.url}/api/now/table/sys_user?sysparm_query=user_name={emailId}"
        response = requests.get(url, headers=self.headers)
        return response.json()

    def deleteRecord(self,table,id):
        print(self.url)
    
    def getAttachments(self,table,id):
        print('')