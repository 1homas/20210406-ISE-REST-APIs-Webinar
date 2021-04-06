# 20210406 ISE REST APIs Webinar


## cURL

### GET/Read resources
```bash
# curl has many options!
curl --help

--head             # headers only
--silent           # disable progress meter/bar
--output <file>    # Write output to <file> instead of stdout
--styled-output    # Enables the automatic use of bold font styles when writing HTTP headers
--verbose          # Makes curl verbose during the operation
```
```bash
# basic HTTP GET request
curl http://ise.securitydemo.net
```
```bash
# Include the HTTP response headers in the output
# Follow redirects
# Allow insecure connections
curl  --include --location --insecure http://ise.securitydemo.net 
```
```bash
# must use HTTP Basic Authentication => 415 Unsupported Media Type
curl \
--include \
--location \
--insecure \
--user admin:C1sco12345 \
https://ise.securitydemo.net:9060/ers/config/endpointgroup
```
```bash
# HTTP Basic Authentication | XML default response
curl \
--include \
--insecure \
--location \
--user admin:C1sco12345 \
--header 'Accept: application/xml' \
https://ise.securitydemo.net:9060/ers/config/endpointgroup
```
```bash
# remove `--include --location`
# For pretty print use linter; is a static code analysis tool for syntax
# use `--silent` to remove the progress bar 
curl \
--silent \
--insecure \
--user admin:C1sco12345 \
--header 'Accept: application/xml' \
https://ise.securitydemo.net:9060/ers/config/endpointgroup \
| xmllint --pretty 1 -
```
```bash
# remove --include; # change to JSON
curl \
--silent \
--insecure \
--user admin:C1sco12345 \
--header 'Accept: application/json' \
https://ise.securitydemo.net:9060/ers/config/endpointgroup
```
```bash
# use `jq` for syntax highlighting
curl \
--silent \
--insecure \
--user admin:C1sco12345 \
--header 'Accept: application/json' \
https://ise.securitydemo.net:9060/ers/config/endpointgroup \
| jq
```
```bash
# use environment variables
curl \
--silent \
--insecure \
--user $ise_rest_username:$ise_rest_password \
--header 'Accept: application/json' \
https://ise.securitydemo.net:9060/ers/config/endpointgroup \
| jq
```
```bash
# GET hotspotportal (only 1) and look at the detail
curl \
--silent \
--insecure \
--user $ise_rest_username:$ise_rest_password \
--header 'Accept: application/json' \
https://ise.securitydemo.net:9060/ers/config/hotspotportal \
| jq
```
```bash
# GET profilerprofile (>600)
curl \
--silent \
--insecure \
--user $ise_rest_username:$ise_rest_password \
--header 'Accept: application/json' \
https://ise.securitydemo.net:9060/ers/config/profilerprofile \
| jq

# GET the end of the profilerprofile list
curl \
--silent \
--insecure \
--user $ise_rest_username:$ise_rest_password \
--header 'Content-Type: application/json' \
--header 'Accept: application/json' \
"https://ise.securitydemo.net:9060/ers/config/profilerprofile?size=100\&page=7" \
| jq
```

### POST/Create a new endpoint
```bash
# find endpointgroup
curl \
--silent \
--include \
--insecure \
--user $ise_rest_username:$ise_rest_password \
--header 'Content-Type: application/json' \
--header 'Accept: application/json' \
https://ise.securitydemo.net:9060/ers/config/endpointgroup \
| jq -c .SearchResult.resources[] \
| grep Meraki -

# Create a new endpoint
curl \
--include \
--insecure \
--user $ise_rest_username:$ise_rest_password \
--header 'Content-Type: application/json' \
--header 'Accept: application/json' \
https://ise.securitydemo.net:9060/ers/config/endpoint \
--data '
{
  "ERSEndPoint" : {
    "name" : "New Endpoint",
    "description" : "My Endpoint",
    "mac" : "FE:ED:DA:DD:BE:EF",
    "staticGroupAssignment" : true,
    "groupId" : "1e2700a0-8c00-11e6-996c-525400b48521"
  }
}'

# Response Header :
# HTTP/1.1 201 
# Location: https://ise.securitydemo.net:9060/ers/config/endpoint/0bd811b0-892f-11eb-b0e1-b2ca5a4c3815
```

### Create a new endpoint with custom attributes
```bash
curl \
--include \
--user $ise_rest_username:$ise_rest_password \
--header 'Content-Type: application/json' \
--header 'Accept: application/json' \
https://ise.securitydemo.net:9060/ers/config/endpoint \
--data @ac17c80c17a2.json

Contents:
{
  "ERSEndPoint" : {
    "name" : "ac:17:c8:0c:17:a2",
    "description" : "camera",
    "mac" : "ac:17:c8:0c:17:a2",
    "groupId" : "1e2700a0-8c00-11e6-996c-525400b48521",
    "staticGroupAssignment" : true,
    "customAttributes" : {
      "customAttributes" : {
        "Authorization" : "surveillance",
        "Owner" : "cameron",
        "Department" : "Security",
        "Device" : "Camera",
        "SerialNumber" : "",
        "Expiration" : "1617493934",
        "Manufacturer" : "Meraki",
        "Model" : "MV12W",
        "Software" : "",
        "Created" : "1616889109"
      }
    }
  }
}
```


### Use POST to create a user
```bash
curl \
--include 
--user $ise_rest_username:$ise_rest_password \
--header 'Content-Type:application/json' \
--header 'Accept: application/json' \
https://$ise_pan:9060/ers/config/internaluser \
--data '
{
    "InternalUser" : {
        "name" : "rigo",
        "password" : "C1sco12345",
        "changePassword" : false
    }
}'
```

### Use POST to create a user from a file
```bash
curl \
--include \
--user $ise_rest_username:$ise_rest_password \
--header 'Content-Type:application/json' \
--header 'Accept: application/json' \
https://$ise_pan:9060/ers/config/internaluser \
--data @data/internaluser.json
```


# Create a Guest user
⚠ Requires `guestapi` user!

```bash
curl \
--include \
--user $guestapi_username:$guestapi_password \
--header 'Content-Type:application/json' \
--header 'Accept: application/json' \
https://$ise_pan:9060/ers/config/guestuser \
--data '
{
    "GuestUser": {
        "guestType": "Daily (default)",
        "portalId" : "bd48c1a1-9477-4746-8e40-e43d20c9f429",
        "guestInfo": {
            "enabled": "true",
            "userName": "rigo",
            "password": "C1sco12345"
        },
        "guestAccessInfo": {
            "validDays": 1,
            "fromDate": "03/27/2021 17:40",
            "toDate": "03/28/2021 17:40",
            "location": "San Jose"
        }
    }
}'
```

### PUT/Update an endpoint
```bash
curl \
--include \
--user $ise_rest_username:$ise_rest_password \
--header 'Content-Type: application/json' \
--header 'Accept: application/json' \
--request PUT https://ise.securitydemo.net:9060/ers/config/endpoint \
--data '
{
  "ERSEndPoint" : {
    "name" : "New Endpoint",
    "description" : "My Endpoint",
    "mac" : "DE:AD:BE:EF:CA:FE",
    "staticGroupAssignment" : true,
    "groupId" : "1e2700a0-8c00-11e6-996c-525400b48521"
  }
}'

# Response Header
# HTTP/1.1 200 
```

### Delete an Endpoint
```bash
curl \
--include \
--user $ise_rest_username:$ise_rest_password \
--header 'Content-Type: application/json' \
--header 'Accept: application/json' \
--request DELETE  https://ise.securitydemo.net:9060/ers/config/endpoint/1b3884b0-8906-11eb-b0e1-b2ca5a4c3815
```


### Other uses of cURL

#### HTTPS Probe for Guest Portal(s)
ISE 2.7+ portal responds with `HTTP/1.1 200` instead of `HTTP/1.1 200 OK`!
curl --include https://ise.securitydemo.net:8443/portal/PortalSetup.action?portal=2c78bb61-1644-416a-a44d-c10b48b9ee47



------------------------------------------------------------------------------



## Postman

### GUI Overview
- New Workspace
- Workspace Name : give your workspace a name
- Collections : your requests for an API
- APIs : Collections & environments with schemas
- Environments : sets of variables for use in context with requests: 
    - Global
    - Environment
    - Collection
    - Local


### Create a GET Request from a curl Request
1. New Collection
1. New Request: 
    1. GET endpointgroup: https://ise.securitydemo.net:9060/ers/config/endpointgroup
        1. Authorization: 
            1. rest_username
            1. rest_password
    1. POST endpointgroup: https://ise.securitydemo.net:9060/ers/config/endpointgroup
        1. Content-Type: application/json
        1. Accept: application/json


### ISE Postman Collections
1. Review https://github.com/1homas/ise-postman-collections
1. import into Postman
1. list all resources and methods
1. GET followed by GET/{id}
    1. Pre-Request
    1. Tests
1. guestuser
    1. fail GET with admin
    1. change environment to dCloud-guestapi
        1. GET guestuser
        1. POST guestuser
        1. DELETE guestuser
1. GET *all* networkdevices
    1. show size / page
    1. open Code Snippet for Python Requests



------------------------------------------------------------------------------



## Python
Install specific Python version and activate virtual environment
```bash
pipenv install --python 3.7
pipenv shell
pipenv install requests
```

Set a RADIUS secondary shared secret on all network devices
```python
#!/usr/bin/env python

import requests
import json

requests.packages.urllib3.disable_warnings()

url = "https://ise.securitydemo.net:9060/ers/config/networkdevice"

payload={}
headers = {
  'Content-Type': 'application/json',
  'Accept': 'application/json',
  'Authorization': 'Basic YWRtaW46QzFzY28xMjM0NQ==',
  'Cookie': 'APPSESSIONID=E1988B8F1CB2EDE0A28253BBE29F1AE7; JSESSIONIDSSO=60629038D127E8CD7F04B058670E3269'
}

resources = []

# get all pages of resources
while (url) :
    # add resources to list
    response = requests.request("GET", url, headers=headers, data=payload, verify=False)
    resources += response.json()["SearchResult"]["resources"]
    try :
        url = response.json()["SearchResult"]["nextPage"]["href"]
    except Exception as e :
        url = None

# loop over resources (networkdevices) to update RADIUS configuration options
for resource in resources :
    # get resource details to update
    url = "https://ise.securitydemo.net:9060/ers/config/networkdevice/"+resource["id"]
    response = requests.request("GET", url, headers=headers, data=payload, verify=False)

    # print networkdevice details
    print(response.json())

    # PUT new RADIUS second shared secret
    networkdevice = response.json()
    print(networkdevice)
    print('----')
    networkdevice["NetworkDevice"]["authenticationSettings"]['enableMultiSecret'] = True
    networkdevice["NetworkDevice"]["authenticationSettings"]['secondRadiusSharedSecret'] = "MySecondSharedSecret"
    payload = json.dumps(networkdevice)
    print('-----')
    response = requests.request("PUT", url, headers=headers, data=payload, verify=False)
    print(response.status_code)
```

