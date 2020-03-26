import csv
import json
import requests

# disable warning for self signed SSL cert
requests.packages.urllib3.disable_warnings()

# required vars
user = '<username>'
passw = '<icauth_pw>'
server = '<servername>'
appname = 'app'
lang = "en-us"


# Connection Request body, header and base URL
body = {'__type': 'urn:inin.com:connection:icAuthConnectionRequestSettings',
        'applicationName' : appname,
        'userID' : user,
        'password' : passw }
header = { 'Accept-Language': lang }
url = f"https://{server}:8019/icws/"

# Connection Request
req = requests.post(url + 'connection', headers=header, data=json.dumps(body), verify=False)

if 'csrfToken' in req.text:
    jreq = json.loads(req.text)
else:
    raise ConnectionError('An error has occurred')

# Get all roles
header['ININ-ICWS-CSRF-Token'] = jreq['csrfToken']
body = {'__type': 'urn:inin.com:connection:icAuthConnectionRequestSettings',
        'applicationName' : appname,
        'sessionId' : jreq['sessionId']}
cookie = req.cookies
req = requests.get(url + jreq['sessionId'] + '/configuration/roles', headers=header, cookies=cookie, data=json.dumps(body), verify=False)

rolereq = json.loads(req.text)
# generate headers for CSV
roles = ['Username']
for i in rolereq['items']:
    roles.append(i['configurationId']['id'])
# get all of the users
req = requests.get(url + jreq['sessionId'] + '/configuration/users', headers=header, cookies=cookie, data=json.dumps(body), verify=False)
userreq = json.loads(req.text)

# get roles for each user
users = []
for u in userreq['items']:
    user = {}
    req = requests.get(url + jreq['sessionId'] + '/configuration/users/' + u['configurationId']['id'] + '?select=roles', headers=header, cookies=cookie, data=json.dumps(body), verify=False)
    ureq = json.loads(req.text)
    user['Username'] = ureq['configurationId']['id']
    if 'effectiveValue' in ureq['roles']:
        for r in ureq['roles']['effectiveValue']:
            user[r['id']] = 'Yes'
    users.append(user)

# writes the csv in the executing directory
with open('usersRoles.csv', 'w', newline='') as csvfile:
    fieldnames = roles
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for u in users:
        writer.writerow(u)

print('jobs done')




    


