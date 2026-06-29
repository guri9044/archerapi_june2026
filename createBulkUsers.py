import csv
import requests
import json

url = "https://archer-irm.com/Archer/platformapi/core/security/login"

requestBody = {
    "InstanceName": "t202603",
    "Username": "api.user",
    "UserDomain": "",
    "Password": "Archer@123"
}
requestHeaders = {
    "Content-Type": "application/json"
}

response = requests.post(url, json=requestBody, headers=requestHeaders)
responseBody = json.loads(response.text)
sessionToken = responseBody["RequestedObject"]["SessionToken"]
print(sessionToken)

url = "https://archer-irm.com/Archer/platformapi/core/system/user"

with open('Users.csv', mode='r', encoding='utf-8-sig') as f:
    users_data = list(csv.DictReader(f))

headers = {
    "Authorization": "Archer session-id=\"" + sessionToken + "\"",
    "Content-Type": "application/json"
}
for user in users_data:
    payload = {
        "User": {
            "UserName": user['Username'],
            "FirstName": user['FirstName'],
            "LastName": user['LastName']
        },
        "Password": user['Password']
    }

    response2 = requests.post(url, json=payload, headers=headers)
    #print(response2.text)
    userbody = json.loads(response2.text)
    userID = userbody["RequestedObject"]["Id"]

    groupIDs = user['Group'].split('/')
    for groupID in groupIDs:
        grouppayload = {
                "UserId":userID,
                "GroupId": groupID,
                "IsAdd":True
            }
        groupurl = "https://archer-irm.com/Archer/platformapi/core/system/usergroup"
        response3 = requests.put(groupurl, json=grouppayload, headers=headers)
        print(response3.text)