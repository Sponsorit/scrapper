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
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--window-size=1920,1080");
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-extensions");
    chrome_options.add_argument("--dns-prefetch-disable");
    chrome_options.add_argument("enable-automation");
    chrome_options.add_argument("--disable-gpu");

    return chrome_options


DRIVER_PATH = './chromedriver'

#For docker
chrome_options = set_chrome_options();
# driver = webdriver.Chrome(options=chrome_options)

#For local
driver = webdriver.Chrome(executable_path=DRIVER_PATH)

dataCollected = {};
validEmailRegex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
headerWritten = False
fileCounter=0.0
rowCounter=0
initialList=2
with open('./twitch_users_'+str(initialList)+'.csv', newline='') as csvfile:
    
    spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
    for row in spamreader:
        
        if row[0] != "user":
            userFound = True
            dataCollected[row[0]]={}
            driver.get('https://twitch.tv/'+row[0])

            try:
                icon =  WebDriverWait(driver,3).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".tw-halo")))
                if(icon.get_attribute("status")=="offline"):
                    if(icon.is_displayed() == False):
                        ActionChains(driver).move_to_element(icon).click(icon).perform()
                    else:
                        icon.click()
            except:
                print("User not found")
                userFound = False
                icon = None
            if userFound:
                try:
                    elems =  WebDriverWait(driver,3).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".social-media-link a[href]")))
                    linksPath = [elem.get_attribute('href') for elem in elems]
                except:
                    print("No social media for this user")
                    linksPath = []
                with open(('twitch_users_networks_'+str(fileCounter)+'.csv'), 'a') as networkFile:
                    if not headerWritten:
                        networkFile.write("user,instagramLink,twitterLink,discordLink\n")
                        headerWritten = True
                    for link in linksPath:
                        if(search("twitter",link)):
                            dataCollected[row[0]]["twitterLink"]=link
                        elif(search("instagram",link)):
                            dataCollected[row[0]]["instagramLink"]=link
                        elif(search("discord",link)):
                            dataCollected[row[0]]["discordLink"]=link
                        
                    networkFile.write("%s,"%(row[0]))
                    if "twitterLink" in dataCollected[row[0]]:
                        networkFile.write("%s"%(dataCollected[row[0]]["twitterLink"]))
                    networkFile.write(",")
                    if "instagramLink" in dataCollected[row[0]]:
                        networkFile.write("%s"%(dataCollected[row[0]]["instagramLink"]))
                    networkFile.write(",")
                    if "discordLink" in dataCollected[row[0]]:
                        networkFile.write("%s"%(dataCollected[row[0]]["discordLink"]))
                    networkFile.write(",")
                    
                        
                    networkFile.write("\n")
                    if rowCounter % 5000 == 0:
                        fileCounter = rowCounter / 5000
                        headerWritten = False
                    rowCounter = rowCounter + 1

