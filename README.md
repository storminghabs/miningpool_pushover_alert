# miningpool_pushover_alert
Simple Python scripts to monitor mining pools and send alerts to Pushover if thresholds are met. Created this to run on a Raspberry Pi but should work on any Linux distro with Python 2.7.

1. Login to Pushover.net or create an account if you don't have one
2. Install the IOS or Android app and login to Pushover
3. Click on "Create a new application/API token"

    Name: Name of mining pool

    Upload a logo if you'd like. These ones work well
    Ethermine: https://play-lh.googleusercontent.com/yJuGQgN-K7Kyk0Vb_aO1Fz2F-i-pIon86JP1DqfBhzMz1Qnbg-OPuTdRdOVXXDvtTd4
    Hiveon: https://cdn-images-1.medium.com/max/1200/1*FcfR0dcdGWBDhtyW2tu86g.png

    Check the checkbox to agree to Terms of Service
4. Download the appropriate script for your mining pool
5. Copy the Token and paste it into the script after PUSHOVER_APP_TOKEN
6. Copy User Key the the main page https://pushover.net/ and paste it into the script after PUSHOVER_USER_TOKEN
7. Paste your ETH wallet address after ETH_ADDRESS
8. Set your minimum MH and worker count
9. Save the Python script and make sure it's set to executable by entering: chmod + x name_of_script.py
10. Run the script: ./name_of_script.py
