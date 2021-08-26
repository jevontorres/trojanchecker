import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import time
import base64
import requests
import json
from twilio.rest import Client

#starts timer to tell how long it took at the end
start = time.time()

#opens a chrome browser without the gui
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")


#driver = webdriver.Chrome(executable_path=os.path.abspath(chrome_path),chrome_options=chrome_options)
trojancheckurl = 'https://trojancheck.usc.edu/login'

usc_user = 'INPUT USC USERNAME no @usc.edu'
usc_pass = 'INPUT BASE64 ENCODED PASSWORD'

usc_pass = base64.b64decode(usc_pass).decode("utf-8") #b64 hashed to prevent shoulder surfing
#usc_pass = 'guest'
phone_number = '+1 ENTER YOUR PHONE NUMBER INCLUDE +1 IF AMERICAN (+14049238493)'
chrome_path = 'INPUT PATH TO CHROMEDRIVER IN DIRECTORY'

#constant xpaths for the elements on the trojancheck site. allows you to id the buttons and boxes
adv_xpath = '/html/body/app-root/app-login/main/section/div/div[1]/div/div[1]/button'
user_xpath = ' //*[@id="username"]'
pass_xpath = ' //*[@id="password"]'
signin_xpath = '//*[@id="loginform"]/div[4]/button'
adv2_xpath = '/html/body/app-root/app-consent-check/main/section/section/button'
onexpath = '/html/body/app-root/app-dashboard/main/div/section[1]/div[2]/button'
twoxpath = '/html/body/app-root/app-assessment-start/main/section[1]/div[2]/button[2]'
no1_xpath = '//*[@id="mat-button-toggle-3-button"]'
no2_xpath = '//*[@id="mat-button-toggle-5-button"]'
submit1_xpath = '/html/body/app-root/app-assessment-questions/main/section/section[3]/button'
no3_xpath = '//*[@id="mat-button-toggle-14-button"]'
no4_xpath = '//*[@id="mat-button-toggle-16-button"]'
no5_xpath = '//*[@id="mat-button-toggle-18-button"]'
no6_xpath = '//*[@id="mat-button-toggle-20-button"]'
no7_xpath = '//*[@id="mat-button-toggle-22-button"]'
no8_xpath = '//*[@id="mat-button-toggle-24-button"]'
no9_xpath = '//*[@id="mat-button-toggle-26-button"]'
submit2_xpath = '/html/body/app-root/app-assessment-questions/main/section/section[8]/button'
check_xpath = '//*[@id="mat-checkbox-1"]/label/div'
submit3_xpath = '/html/body/app-root/app-assessment-review/main/section/section[11]/button'

#makes the window the size of the average phone
driver = webdriver.Chrome(options=chrome_options)
driver.set_window_size(376, 812)
#driver = webdriver.Chrome(chrome_path)

#goes to trojancheck site and signs in
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

#first page after signin
driver.find_element_by_xpath(onexpath).click()
time.sleep(2)
driver.find_element_by_xpath(twoxpath).click()
time.sleep(2)

#second page after signin, starts to ask about covid
driver.find_element_by_xpath(no1_xpath).click()
driver.find_element_by_xpath(no2_xpath).click()
driver.find_element_by_xpath(submit1_xpath).click()
time.sleep(2)

#third page after signin, asks about symptoms
driver.find_element_by_xpath(no3_xpath).click()
driver.find_element_by_xpath(no4_xpath).click()
driver.find_element_by_xpath(no5_xpath).click()
driver.find_element_by_xpath(no6_xpath).click()
driver.find_element_by_xpath(no7_xpath).click()
driver.find_element_by_xpath(no8_xpath).click()
driver.find_element_by_xpath(no9_xpath).click()
driver.find_element_by_xpath(submit2_xpath).click()
time.sleep(2)

#fourth page after signin, asks if you were telling the truth and to verify answers
driver.find_element_by_xpath(check_xpath).click()
driver.find_element_by_xpath(submit3_xpath).click()
time.sleep(2)

#scrolls down to the part you want to see, the qr code and color
for i in range(14): #10 with window 13 headless
    driver.find_element_by_tag_name("html").send_keys(Keys.DOWN)
driver.save_screenshot('trojancheck.png')
time.sleep(1)

#base64 encodes and upload image to public site, saves image url
with open("trojancheck.png", "rb") as file:
    url = "https://api.imgbb.com/1/upload"
    payload = {
        "key": 'IMGBBAPIKEY',
        "image": base64.b64encode(file.read()),
    }
    res = requests.post(url, payload)
    objj = res.json()
image_link = objj["data"]["url"]

#texts the image (which will show up as image and not just link)
account_sid = 'TWILIO ACCOUNTSID'
auth_token = 'TWILIO AUTHTOKEN'
client = Client(account_sid, auth_token)

message = client.messages \
    .create(
         #body='This is the ship that made the Kessel Run in fourteen parsecs?',
         from_='TWILIO FROM NUMBER',
         media_url=[image_link],
         to=phone_number
     )

end = time.time()
print(message.sid)
print("SENT, took",end-start,"seconds")
