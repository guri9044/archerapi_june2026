import requests
import json
import os
sessionToken = os.getenv('archerPAT')

url = "https://archer-irm.com/Archer/platformapi/core/security/login"

payload = json.dumps({
  "InstanceName": "t202603",
  "Username": "api.user",
  "UserDomain": "",
  "Password": "Archer@123"
})
headers = {
  'Content-Type': 'application/json'
}

response = requests.post(url, headers=headers, data=payload)

v = json.loads(response.text)
sessionToken = v["RequestedObject"]["SessionToken"]
print(sessionToken)