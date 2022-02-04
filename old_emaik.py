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
dataCollected = {};
validEmailRegex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

with open('twitch_users.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
    for row in spamreader:
        if row[0] != "user":
            dataCollected[row[0]]={}
            driver.get('https://twitch.tv/'+row[0])
            time.sleep(1)
            icon = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".tw-halo")))
            if(icon.get_attribute("status")=="offline"):
                if(icon.is_displayed() == False):
                    ActionChains(driver).move_to_element(icon).click(icon).perform()
                else:
                    icon.click()
            time.sleep(2)
            elems = WebDriverWait(driver,10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a[href]")))
            linksPath = [elem.get_attribute('href') for elem in elems]
            for link in linksPath:
                if(search("twitter",link)):
                    driver.get(link)
                    dataCollected[row[0]]["twitterLink"]=link
                    descriptionSpans = WebDriverWait(driver,10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div[data-testId='UserDescription'] span")))
                    for span in descriptionSpans:
                        spanText = span.text
                        dataCollected[row[0]]["twitterBussinesEmail"]=re.findall(r'[\w.+-]+@[\w-]+\.[\w.-]+', spanText)
                elif(search("instagram",link)):
                    dataCollected[row[0]]["instagramLink"]=link
                elif(search("discord",link)):
                    dataCollected[row[0]]["discordLink"]=link
                

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
for user in dataCollected:
    driver.get(dataCollected[user]["instagramLink"])
    descriptionSpans = WebDriverWait(driver,10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "header section div:last-of-type span")))
    for span in descriptionSpans:
        spanText = span.text

        
        dataCollected[row[0]]["instagramBussinesEmail"]=re.findall(r'[\w.+-]+@[\w-]+\.[\w.-]+', spanText)

f = open('twitch_users_email.csv', 'w')
writer = csv.writer(f)

writer.writerow(row)

f.close()
print(dataCollected)