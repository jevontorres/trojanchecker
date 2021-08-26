import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import time
import base64
import requests
import json
from twilio.rest import Client

start = time.time()


chrome_options = Options()
chrome_options.add_argument("--headless") #work without showing browser

#b'TWFyY29XYWxsczAwVVNDJCQ='
#constant pathids, urls and credentials
trojancheckurl = 'https://trojancheck.usc.edu/login'

usc_user = 'input username'
usc_pass = 'base64 your password'
phone_number = '+1 number'
usc_pass = base64.b64decode(usc_pass).decode("utf-8") #b64 hashed to prevent shoulder surfing
chrome_path = 'path to chromedriver'
adv_xpath = '/html/body/app-root/app-login/main/section/div/div[1]/div/div[1]/button'
user_xpath = ' //*[@id="username"]'
pass_xpath = ' //*[@id="password"]'
signin_xpath = '//*[@id="loginform"]/div[4]/button'
adv2_xpath = '/html/body/app-root/app-consent-check/main/section/section/button'

driver = webdriver.Chrome(executable_path=os.path.abspath('chromedriver'),chrome_options=chrome_options)
#driver = webdriver.Chrome(chrome_path)
driver.set_window_size(376, 812) #make it look like iphone for screenshot later


#advance through website up to test, pause for internet issues
driver.get(trojancheckurl)
time.sleep(2)
driver.find_element_by_xpath(adv_xpath).click() #go to sso
time.sleep(2)
driver.find_element_by_xpath(user_xpath).send_keys(usc_user)
driver.find_element_by_xpath(pass_xpath).send_keys(usc_pass)
driver.find_element_by_xpath(signin_xpath).click()
time.sleep(2)
driver.find_element_by_xpath(adv2_xpath).click()
time.sleep(2)

#actually take the test IMPLEMENT TBD

#scroll down and take screenshot
for i in range(14): #10 with window 13 headless
	driver.find_element_by_tag_name("html").send_keys(Keys.DOWN) #scroll down a little bit
driver.save_screenshot('trojancheck.png')
time.sleep(1)


#base64 and upload image
with open("trojancheck.png", "rb") as file:
    url = "https://api.imgbb.com/1/upload"
    payload = {
        "key": 'IMGBB APIKEY',
        "image": base64.b64encode(file.read()),
    }
    res = requests.post(url, payload)
    objj = res.json()
image_link = objj["data"]["url"]


#text it to me
account_sid = 'TWILIO SID'
auth_token = 'TWILIO TOKEN'
client = Client(account_sid, auth_token)

message = client.messages \
    .create(
         #body='This is the ship that made the Kessel Run in fourteen parsecs?',
         from_='TWILIO FROM NUMBER',
         media_url=[image_link],
         to=phone_number
     )


end = time.time()
print(message.sid) #not really neccesary, comes from text/twilio
print("SENT, took",end-start,"seconds")
