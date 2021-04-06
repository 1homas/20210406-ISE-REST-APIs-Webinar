#!/usr/bin/env python
# ----------------------------------------------------------------------------
# Python script to update all ISE networkdevices with a second shared secret.
#
# Author: Thomas Howard, thomas@cisco.com
# Cisco Sample Code License: 
# https://developer.cisco.com/site/license/cisco-sample-code-license/
# ----------------------------------------------------------------------------

import requests
import json

url = "https://ise.securitydemo.net:9060/ers/config/networkdevice"

payload={}

# You will need to update the Authorization & Cookie headers for your ISE!
# These were generated from a Postman code snippet.
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
    # print(response.json())

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
