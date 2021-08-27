# TrojanChecker

A simple app to automate the authentication and form responses needed for daily Trojan Check approval.

## Notes and Status

Currently implemented and scheduled on PythonAnywhere for a single user, me ;) . Plans for the very near future include allowing multiple users and providing a seamless and secure sign-up process. 

## Liability / Terms and Conditions ?

I am in no way responsible for your honesty, or lack thereof, through the use of this program or close variants of it. Each time you run this application with your credentials, you are ensuring that responses of 0 COVID symptoms or positive tests are all true. To elucidate, do not use this program and forget that it is running, do not use this program if you have any symptoms of any sickness, and do not use this program with the knowledge or assumption of a present or future positive COVID test. 

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install selenium and twilio.

```bash
pip install selenium
pip install twilio
```

## Usage
Make a file in directory called users.txt with format "username password phonenumber" separate each word with a space and each user with a new line. **PHONE NUMBER MUST BE WITH COUNTRY CODE** i.e +1. 

In the trojanchecke(r/d).py, edit anything marked to be changed. This includes, your USC username and password (base64 encoded), your phone number, directory path to chromedriver, imgbb API keys, and twilio account SID and auth token. These were removed for obvious security reasons.

To complete the check and recieve a text with the code and color, run checker.
```bash
python trojanchecker.py
```
If you have completed the check already and want the picture again, run checked.
```bash
python trojanchecked.py
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)