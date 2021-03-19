import time
from selenium import webdriver
from selenium.webdriver.support.ui import Select
import sys
from io import StringIO
import contextlib
import yeelight
import random
import time

password = random.randint(1000, 100000)

bulb = yeelight.Bulb("192.168.1.176")

WEBDRIVER = "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(WEBDRIVER)

link = input("Please enter the google meet url.")

# Opens google login and input email and password
driver.get("https://accounts.google.com/signin/v2/identifier?service=accountsettings&continue=https%3A%2F%2Fmyaccount.google.com%3Futm_source%3Daccount-marketing-page%26utm_medium%3Dgo-to-account-button&flowName=GlifWebSignIn&flowEntry=ServiceLogin")
time.sleep(1)
driver.find_element_by_xpath('//*[@id="identifierId"]').send_keys("EMAIL HERE\n") # Change this
time.sleep(1)
driver.find_element_by_xpath('//*[@id="password"]/div[1]/div/div[1]/input').send_keys("PASSWORD HERE\n") # Change this
time.sleep(2)
driver.get(link)
input("\n\n\nPRESS ENTER TO CONTINUE\n\n\n")

@contextlib.contextmanager
def stdoutIO(stdout=None):
    old = sys.stdout
    if stdout is None: stdout = StringIO()
    sys.stdout = stdout
    yield stdout
    sys.stdout = old

def evalPrint(thing):
    with stdoutIO() as s:
        try: exec(thing, {"sleep": time.sleep})
        except Exception as e: return f"And error occured:\n{e}"
        evaled = s.getvalue()
        return evaled

def process_message(message):
    if message != None or message != "":
        output = ""

        try:
            # if message.lower()[0:4] == "!say": output = message[5::]
            if message.lower()[0:3] == "!py": output = evalPrint(message[4::])
            # elif message.lower() == "!lights": bulb.toggle(); output = "Lights have been toggled."
            else: output = None
        except: output = None

        return output

def get_message():
    try:
        messages = driver.find_element_by_xpath('//*[@id="ow3"]/div[1]/div/div[8]/div[3]/div[4]/div/div[2]/div[2]/div[2]/span[2]/div').find_elements_by_class_name("GDhqjd")
        latestMessage = messages[-1].find_element_by_class_name("Zmm6We").find_elements_by_class_name("oIy2qc")[-1].get_property("innerHTML")
        # user = latestMessage = messages[-1].find_element_by_class_name("Zmm6We").find_elements_by_class_name("oIy2qc")[0]
        return latestMessage
    except: return None

def send_message(message):
    if message != None or message != "":
        messageBox = driver.find_element_by_xpath('//*[@id="ow3"]/div[1]/div/div[8]/div[3]/div[4]/div/div[2]/div[2]/div[2]/span[2]/div/div[3]/div[1]/div[1]/div[2]/textarea')
        button = driver.find_element_by_xpath('//*[@id="ow3"]/div[1]/div/div[8]/div[3]/div[4]/div/div[2]/div[2]/div[2]/span[2]/div/div[3]/div[2]')

        messageBox.send_keys(message)
        button.click()

while True:
    print(f"------- Bot loop ------- {password}")
    message = get_message()
    print(message)
    response = process_message(message)
    print(response)
    if response == None or response == "": pass
    else: send_message(response)
    time.sleep(0.5)
