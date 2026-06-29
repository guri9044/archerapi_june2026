import requests

url = "https://archer-irm.com/Archer/ws/general.asmx/CreateUserSessionFromInstance"

payload = 'userName=api.user&instanceName=t202603&password=Archer%40123'
headers = {
  'Content-Type': 'application/x-www-form-urlencoded'
}

response = requests.post(url, headers=headers, data=payload)

print(response.text)
