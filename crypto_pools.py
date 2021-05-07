import requests
import httplib2, urllib
import json

class pool_monit:
    def __init__(self, url, pool_name,PUSHOVER_APP_TOKEN,PUSHOVER_USER_TOKEN,alert=False):
        self.url = url
        self.pool_name = pool_name
        self.alert = alert
        self.averageHashrate =0
        self.currentHashrate  =0
        self.reportedHashrate  =0
        self.activeWorkers  =0
        self.MINIMUM_REPORTED_MH = "600"
        self.MINIMUM_WORKERS = "6"
        self.PUSHOVER_APP_TOKEN = PUSHOVER_APP_TOKEN
        self.PUSHOVER_USER_TOKEN = PUSHOVER_USER_TOKEN
        self.data = {}

    def pull_data(self):
        response = requests.get(self.url)
        if response.status_code != 200:
            print('error {}'.format(response.status_code))
        else:
            data = json.loads(response.text)
            data = json.dumps(data, indent=4)
            self.eth_data = json.loads(data)
            return True

        return False

    def calculate_has_rate(self):
        pass

    def print_hash_rate(self):
        print("Average: "), self.averageHashrate
        print("Current: "), self.currentHashrate
        print("Reported: "), self.reportedHashrate
        print("Active workers: "), self.activeWorkers

        if self.reportedHashrate < int(self.MINIMUM_REPORTED_MH):
            self.alert = True
            alertMessage = alertMessage + "Reported hashrate is below threshold\n"
            print("Reported MH is under")

        if self.activeWorkers < int(self.MINIMUM_WORKERS):
            self.alert = True
            self.alertMessage = alertMessage + "Current worker count is below threshold"
            print("Active workers is below")

    def alert(self):
        if self.alert == True:
            conn = httplib2.HTTPSConnection("api.pushover.net:443")
            conn.request("POST", "/1/messages.json",
                         urllib.urlencode({
                             "token": self.PUSHOVER_APP_TOKEN,
                             "user": self.PUSHOVER_USER_TOKEN,
                             "title": self.pool_name+" alert",
                             "message": self.alertMessage,
                         }), {"Content-type": "application/x-www-form-urlencoded"})
            conn.getresponse()


class pool_hiveon(pool_monit):
    def __init__(self, url,ETH_ADDRESS,PUSHOVER_APP_TOKEN,PUSHOVER_USER_TOKEN,alert=False):
        url = url + ETH_ADDRESS.lower() + "/ETH"
        super().__init__(url, 'Hiveon',PUSHOVER_APP_TOKEN,PUSHOVER_USER_TOKEN,alert)

    def calculate_has_rate(self):
        self.averageHashrate = round (int(self.eth_data['hashrate24h']) / 1000000, 2)
        self.currentHashrate = round (int(self.eth_data['hashrate']) / 1000000, 2)
        self.reportedHashrate = round (int(self.eth_data['reportedHashrate']) / 1000000, 2)
        self.activeWorkers = int(self.eth_data['onlineWorkerCount'])


class pool_ethermine(pool_monit):
    def __init__(self, url,ETH_ADDRESS,PUSHOVER_APP_TOKEN,PUSHOVER_USER_TOKEN, alert=False):
        url = url + ETH_ADDRESS + "/currentStats"
        super().__init__(url, 'Ethermine',PUSHOVER_APP_TOKEN,PUSHOVER_USER_TOKEN, alert)

    def calculate_has_rate(self):
        self.averageHashrate = round(int(self.eth_data['data']['averageHashrate']) / 1000000, 2)
        self.currentHashrate = round(int(self.eth_data['data']['currentHashrate']) / 1000000, 2)
        self.reportedHashrate = round(int(self.eth_data['data']['reportedHashrate']) / 1000000, 2)
        self.activeWorkers = int(self.eth_data['data']['activeWorkers'])


