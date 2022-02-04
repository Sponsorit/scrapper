from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait     
from selenium.webdriver.common.by import By     
from selenium.webdriver.common.action_chains import ActionChains

import csv
import time
from re import search
import re

DRIVER_PATH = '/home/vlad/Descargas/chromedriver_linux64/chromedriver'
driver = webdriver.Chrome(executable_path=DRIVER_PATH)

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

dataCollected = {}
headerWritten= False
with open('./twitch_users_networks.csv', newline='') as csvfile:
    with open('twitch_users_emails.csv', 'w') as emailsFile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        if not headerWritten:
            emailsFile.write("user,instagramEmail,twitterEmail,\n");
            headerWritten = True
        for row in spamreader:
                if row[0] != "user":
                    dataCollected[row[0]]={}
                    emailsFile.write(row[0]+",")

                    if(row[2] is not ''):
                        driver.get(row[2])
                        descriptionSpans = WebDriverWait(driver,10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "header section div:last-of-type span")))
                        for span in descriptionSpans:
                            spanText = span.text
                            dataCollected[row[0]]["instagramBussinesEmail"]=re.findall(r'[\w.+-]+@[\w-]+\.[\w.-]+', spanText)
                        if "instagramBussinesEmail" in dataCollected[row[0]]:
                            emailsFile.write("%s"%(dataCollected[row[0]]["instagramBussinesEmail"]))
                        emailsFile.write(",")
                    if(row[1] is not ''):
                        driver.get(row[1])
                        descriptionSpans = WebDriverWait(driver,10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div[data-testId='UserDescription'] span")))
                        for span in descriptionSpans:
                            spanText = span.text
                            dataCollected[row[0]]["twitterBussinesEmail"]=re.findall(r'[\w.+-]+@[\w-]+\.[\w.-]+', spanText)
                        if "twitterBussinesEmail" in dataCollected[row[0]]:
                            emailsFile.write("%s"%(dataCollected[row[0]]["twitterBussinesEmail"]))
                        emailsFile.write(",")

                    emailsFile.write("\n")
                    



