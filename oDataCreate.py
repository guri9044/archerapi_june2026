import requests
import json

url = "https://archer-irm.com/Archer/contentapi/Findings"

payload = json.dumps({
  "Findings_Id": 435857,
  "Name":"oData Finding 125",
  "Finding": "oData 52 During testing, it was determined that this control is considered not in place."
})
headers = {
  'Cookie': '__ArcherSessionCookie__=FF1A8A595C9D496F08C3DA754464B12A',
  'Content-Type': 'application/json',
  'x_csrf_token':'u14Q7CG1HUP7axrCuZWRD2nX4hh4B1b1ax0TLUOURNHsLZ1U357OeuWKSwebqR4_vR-zhl_V6wkMrtK9WubuuuxwGV1M6x5p2d5unDIUs741',

}

response = requests.post(url, headers=headers, data=payload)

print(response)
