#!/usr/bin/env python
import requests
import httplib, urllib
import json

ETH_ADDRESS = "ETH WALLET ADDRESS"
MINIMUM_REPORTED_MH = "600"
MINIMUM_WORKERS = "6" 
PUSHOVER_APP_TOKEN = "PUSHOVER APP TOKEN"
PUSHOVER_USER_TOKEN = "PUSHOVER USER TOKEN"

#Resetting variables
alertMessage = ("")
Alert = False

url = "https://api.ethermine.org/miner/" + ETH_ADDRESS + "/currentStats"

response = requests.get(url)
if response.status_code != 200:
    print('error {}'.format(response.status_code))
else:
    data = json.loads(response.text)
    data = json.dumps(data, indent=4)
    eth_data = json.loads(data)

    averageHashrate = int(eth_data['data']['averageHashrate'])/1000000
    currentHashrate = int(eth_data['data']['currentHashrate'])/1000000
    reportedHashrate = int(eth_data['data']['reportedHashrate'])/1000000
    activeWorkers = int(eth_data['data']['activeWorkers'])

    averageHashrate = round(averageHashrate,2)
    currentHashrate = round(currentHashrate,2)
    reportedHashrate = round(reportedHashrate,2)

    print ("Average: "), averageHashrate
    print ("Current: "), currentHashrate
    print ("Reported: "), reportedHashrate
    print ("Active workers: "), activeWorkers

    if reportedHashrate < int(MINIMUM_REPORTED_MH):
      Alert = True
      alertMessage = alertMessage + "Reported hashrate is below threshold\n"
      print ("Reported MH is under")

    if activeWorkers < int(MINIMUM_WORKERS):
      Alert = True
      alertMessage = alertMessage + "Current worker count is below threshold"
      print ("Active workers is below")

if Alert == True:
   conn = httplib.HTTPSConnection("api.pushover.net:443")
   conn.request("POST", "/1/messages.json",
      urllib.urlencode({
            "token": PUSHOVER_APP_TOKEN,
            "user": PUSHOVER_USER_TOKEN,
            "title": "Ethermine alert",
            "message": alertMessage,
       }), { "Content-type": "application/x-www-form-urlencoded" })
   conn.getresponse()
