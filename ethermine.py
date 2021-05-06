#!/usr/bin/env python  #TODO:  Consider:  Not all users will have python3 at this path.

# TODO: Make sure you're using python3.  2.7 is deprecated now.  (Looks like you wrote for 3)



import requests
import httplib
import urllib  #TODO:  Ok to import with commas but I don't think people do it as much these days without a 'from' style import.  I may be wrong
import json

def append_alert_message(existing_alert_messages, new_alert_message):
    """
    Appends new_alert_message (a string) to existing_alert_messages (also a string of new-line separated messages)
    :param existing_alert_messages: A string with all the previous messages on it
    :param new_alert_message: Another string to append onto existing_alert_messages
    :return:
    """

    if existing_alert_messages == "":
        ret_val = new_alert_message
    else:
        ret_val = f"{existing_alert_messages}\n{new_alert_message}"

    return ret_val


ETH_ADDRESS = "ETH WALLET ADDRESS"
MINIMUM_REPORTED_MH = "600"  # TODO:  Should this be string, or int?
MINIMUM_WORKERS = "6"   # TODO:  Should this be string, or int?
PUSHOVER_APP_TOKEN = "PUSHOVER APP TOKEN"
PUSHOVER_USER_TOKEN = "PUSHOVER USER TOKEN"

def main():
    """
    This is the main program
    :return:
    """

    #making sure alert message is empty
    alert_message = ("")  #TODO:  This is a tuple (immutable iterable) with a single value in it (an empty string).  Is this what you want or just a string?

    # url = "https://api.ethermine.org/miner/" + ETH_ADDRESS + "/currentStats"  #TODO:  Line commented out to show f-string formatting below
    url = f"https://api.ethermine.org/miner/{ETH_ADDRESS}/currentStats"  #TODO:  This is called f-string formatting and I think it's easier.  Personal preference though

    response = requests.get(url)
    if response.status_code != 200:
        print('error {}'.format(response.status_code))  #TODO:  Consider f-string
    else:
        data = json.loads(response.text)
        data = json.dumps(data, indent=4)  #TODO:  Love to use the indent arg to proce pretty printing
        eth_data = json.loads(data)

        # eth_data = json.loads(response.text)  # TODO:  This line should do the same as the three above it.
                                                # TODO:  Note that Python lists and dicts map perfectly to JSON with one eception:
                                                # TODO:  Python allows for strings to be in either single or double quotes
                                                # TODO:  While JSON calls for double quotes only.  The json.loads() and json.dumps()
                                                # TODO:  Methods account for this.  Loading, then dumoing, then re-loading essentially causes
                                                # TODO:  Single quotes to be coerced to double


        # averageHashrate = int(eth_data['data']['averageHashrate'])/1000000 # TODO:  Commented out in favor of snake_case
        # currentHashrate = int(eth_data['data']['currentHashrate'])/1000000 # TODO:  Commented out in favor of snake_case
        # reportedHashrate = int(eth_data['data']['reportedHashrate'])/1000000 # TODO:  Commented out in favor of snake_case
        # activeWorkers = int(eth_data['data']['activeWorkers']) # TODO:  Commented out in favor of snake_case

        average_hash_rate = int(eth_data['data']['averageHashrate'])/1000000  # TODO:  Favor lower_snake_case over camelCase.  It is considered more pythonic.
        current_hash_rate = int(eth_data['data']['currentHashrate'])/1000000  # TODO:  Favor lower_snake_case over camelCase.  It is considered more pythonic.
        reported_hash_rate = int(eth_data['data']['reportedHashrate'])/1000000  # TODO:  Favor lower_snake_case over camelCase.  It is considered more pythonic.
        active_workers = int(eth_data['data']['activeWorkers'])  # TODO:  Favor lower_snake_case over camelCase.  It is considered more pythonic.

        # TODO:  You could wrap the int(.....) lines above in round(int(.....)) to do this all in one go if you wanted
        average_hash_rate = round(average_hash_rate, 2)
        current_hash_rate = round(current_hash_rate, 2)
        reported_hash_rate = round(reported_hash_rate, 2)

        print("Average: "), average_hash_rate  #TODO:  Would go for f-strings here, but that's just me
        print("Current: "), current_hash_rate  #TODO:  Would go for f-strings here, but that's just me
        print("Reported: "), reported_hash_rate  #TODO:  Would go for f-strings here, but that's just me
        print("Active workers: "), active_workers  #TODO:  Would go for f-strings here, but that's just me

        if reported_hash_rate < int(MINIMUM_REPORTED_MH):
          alert = True
          alert_message = alert_message + "Reported hashrate is below threshold\n"
          print("Reported MH is under")

        #TODO:  Nothing wrong with the way you're handling newlines above but the way I usually do it is this
        # You won't wind up with trailing newlines:
        # TODO:  Start of alternative block:
        if reported_hash_rate < int(MINIMUM_REPORTED_MH):
            if alert_message == "":
                alert_message = "Reported hashrate is below threshold"
            else:
                alert_message = f"{alert_message}\nReported hashrate is below threshold"
        # TODO:  End of alternative block:

        if active_workers < int(MINIMUM_WORKERS):  #TODO: See question about MINIMUM_WORKERS being int or str at top of program
          alert = True  #TODO:  You've got some pep8 warning about indentation pycharm is bubbling up here and in other spots (I say, use tabs and not spaces).  See:  https://www.flake8rules.com/rules/E111.html
          alert_message = alert_message + "Current worker count is below threshold"  #TODO:  Since you're appending to alert message in more than once place, it would probably make sense to introduce a function that handle is.  I've added one as an example at the top
          print ("Active workers is below")

          # TODO:  Example of how you might append a new alert message using the function at the top of program:
          # TODO:  Start of example of function
          msg = "Current worker count is below threshold"
          alert_message = append_alert_message(existing_alert_messages=alert_message, new_alert_message=msg)
          # TODO:  End example of function


    # if alert == True:  #TODO:  This is technically incorrect although it will run.  With booleans we use 'is' and not '=='
    if alert is True:  # TODO.  Use 'is'
       conn = httplib.HTTPSConnection("api.pushover.net:443")
       conn.request("POST", "/1/messages.json",
          urllib.urlencode({
                "token": PUSHOVER_APP_TOKEN,
                "user": PUSHOVER_USER_TOKEN,
                "title": "Ethermine alert",
                "message": alert_message,
           }), { "Content-type": "application/x-www-form-urlencoded" })
       conn.getresponse()


if __name__ == "__main__":
    """
    Invokes the main program if this .py file is invoked (as opposed to imported) directly
    """

    # TODO:  This bit of boilerplate code allows your program to be used as a standalone program or as an importable module
    # TODO:  See:  https://tinyurl.com/yes8ayrk
    # TODO:  See:  https://tinyurl.com/oj246f4
    main()