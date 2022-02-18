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
    chrome_options.add_argument("headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-extensions");
    chrome_options.add_argument("--dns-prefetch-disable");
    chrome_options.add_argument("enable-automation");
    chrome_options.add_argument("--disable-gpu");
    chrome_options.binary_location="/usr/bin/google-chrome-stable";

    return chrome_options


DRIVER_PATH = './chromedriver98'

#For docker
chrome_options = set_chrome_options();

driver = webdriver.Chrome(options=chrome_options,executable_path=DRIVER_PATH)

logedIn=False
def logInsta(driver):
    try:
        driver.get("https://www.instagram.com/accounts/login/")
        time.sleep(1)
        cookiesButton = WebDriverWait(driver,10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div[role='dialog'] button")))[0]
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
with open('./twitch_users_networks_total.csv', newline='') as csvfile:
    with open('twitch_users_emails.csv', 'w') as emailsFile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        if not headerWritten:
            emailsFile.write("user,instagramEmail,twitterEmail,\n");
            headerWritten = True
        for row in spamreader:
            if not LogedIn:
                LogedIn = logInsta(driver)
            if LogedIn:
                userName = row[0]
                    if userName != "user":
                        dataCollected[userName]={}
                        emailsFile.write(userName+",")

                        if(row[2] is not ''):
                            driver.get(row[2])
                            descriptionSpans = WebDriverWait(driver,3).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "header section div:last-of-type span")))
                            for span in descriptionSpans:
                                spanText = span.text
                                dataCollected[row[0]]["instagramBussinesEmail"]=re.findall(r'[\w.+-]+@[\w-]+\.[\w.-]+', spanText)
                            if "instagramBussinesEmail" in dataCollected[row[0]]:
                                emailsFile.write("%s"%(dataCollected[row[0]]["instagramBussinesEmail"]))
                            emailsFile.write(",")
                        if(row[1] is not ''):
                            driver.get(row[1])
                            descriptionSpans = WebDriverWait(driver,3).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div[data-testId='UserDescription'] span")))
                            for span in descriptionSpans:
                                spanText = span.text
                                dataCollected[row[0]]["twitterBussinesEmail"]=re.findall(r'[\w.+-]+@[\w-]+\.[\w.-]+', spanText)
                            if "twitterBussinesEmail" in dataCollected[row[0]]:
                                emailsFile.write("%s"%(dataCollected[row[0]]["twitterBussinesEmail"]))
                            emailsFile.write(",")

                        emailsFile.write("\n")
                    
driver.quit()


