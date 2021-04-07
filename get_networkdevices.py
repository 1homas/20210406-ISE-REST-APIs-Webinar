#!/usr/bin/env python
# ----------------------------------------------------------------------------
# Python script to print a list of all ISE networkdevice ids and names.
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

# loop over URLs
while (url) :
    # add resources to list
    response = requests.request("GET", url, headers=headers, data=payload, verify=False)
    resources += response.json()["SearchResult"]["resources"]
    try :
        url = response.json()["SearchResult"]["nextPage"]["href"]
    except Exception as e :
        url = None

# loop over resources (networkdevices)
for resource in resources :
    # print resource names
    print(f'{resource["id"]} {resource["name"]}')
