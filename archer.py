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

    def createRecords(self,data):
        print()

        