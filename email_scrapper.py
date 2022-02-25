from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait     
from selenium.webdriver.common.by import By     
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options

import csv
import time
from re import search
import re
from selenium.common.exceptions import NoSuchElementException      

def set_chrome_options() -> None:
    """Sets chrome options for Selenium.
    Chrome options for headless browser is enabled.
    """
    chrome_options = Options()
    # chrome_options.add_argument("headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-extensions");
    chrome_options.add_argument("--dns-prefetch-disable");
    chrome_options.add_argument("enable-automation");
    chrome_options.add_argument("--disable-gpu");
    chrome_options.binary_location="/usr/bin/google-chrome-stable";

    return chrome_options


DRIVER_PATH = './chromedriver97'

#For docker
chrome_options = set_chrome_options();

driver = webdriver.Chrome(options=chrome_options,executable_path=DRIVER_PATH)

logedIn=False
def logInsta(driver):
    try:
        driver.get("https://www.instagram.com/accounts/login/")
        time.sleep(1)
        cookiesButton = WebDriverWait(driver,10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div[role='dialog'] .aOOlW")))[0]
        print(cookiesButton)
        ActionChains(driver).move_to_element(cookiesButton).click(cookiesButton).perform()
        time.sleep(1)
        user = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='username']")))
        password = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='password']")))
        loginButton = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "button[type='submit']")))
        user.send_keys("vladi2811@protonmail.com")
        password.send_keys("patataasada11")
        ActionChains(driver).move_to_element(loginButton).click(loginButton).perform()
        time.sleep(1)
        rememberLogButton = WebDriverWait(driver,10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "main section button")))[0]
        ActionChains(driver).move_to_element(rememberLogButton).click(rememberLogButton).perform()
        time.sleep(1)
        return True
    except:
        return False
dataCollected = {}
headerWritten= False
loggedFirstLog = False
LogedIn=False

with open('./allNetworks25feb.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    
    for row in spamreader:
        
        if not LogedIn:
            print("Not logged in")
            LogedIn = logInsta(driver)
        if LogedIn:
            if not loggedFirstLog:
                print("Logged In")
                loggedFirstLog = True
            userName = row[0]
            print(userName)
            if userName != "user":
                dataCollected[userName]={}
                with open('./twitch_users_emails_data.csv', 'a') as emailsFile:
                    if not headerWritten:
                        emailsFile.write("user,instagramEmail,twitterEmail,\n");
                        print("Headder written")
                        headerWritten = True
                    emailsFile.write(userName+",")
                    
                    if(row[2] is not ''):
                        try:
                            driver.get(row[2])
                            descriptionSpans = WebDriverWait(driver,3).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "header section div:last-of-type span")))
                            for span in descriptionSpans:
                                spanText = span.text
                                dataCollected[row[0]]["instagramBussinesEmail"]=re.findall(r'[\w.+-]+@[\w-]+\.[\w.-]+', spanText)
                            if "instagramBussinesEmail" in dataCollected[row[0]]:
                                emailsFile.write("%s"%(dataCollected[row[0]]["instagramBussinesEmail"]))
                            emailsFile.write(",")
                        except:
                            print("Invalid instagram link")
                    if(row[1] is not ''):
                        try:
                            driver.get(row[1])
                            descriptionSpans = WebDriverWait(driver,3).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div[data-testId='UserDescription'] span")))
                            for span in descriptionSpans:
                                spanText = span.text
                                dataCollected[row[0]]["twitterBussinesEmail"]=re.findall(r'[\w.+-]+@[\w-]+\.[\w.-]+', spanText)
                            if "twitterBussinesEmail" in dataCollected[row[0]]:
                                emailsFile.write("%s"%(dataCollected[row[0]]["twitterBussinesEmail"]))
                            emailsFile.write(",")
                        except:
                            print("Invalid Twitter link")

                    emailsFile.write("\n")
                    
driver.quit()


