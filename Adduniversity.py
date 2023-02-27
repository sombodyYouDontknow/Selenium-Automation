from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException,StaleElementReferenceException
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from config import Usernmae,Password
import pandas as pd
import time

df = pd.read_excel('universities.xlsx')



browser = webdriver.Chrome(executable_path="C:\chromedriver\chromedriver")

browser.get('http://afterplustwo.org/admin/')
time.sleep(2)
username_field = browser.find_element(By.ID,"email")
username_field.send_keys(Usernmae)
password_field = browser.find_element(By.ID,"password")
password_field.send_keys(Password)
login = browser.find_element(By.NAME,"btnLogin")
login.submit()
university = browser.find_element(By.LINK_TEXT,"Universities").click()
adduni = browser.find_element(By.LINK_TEXT,"Add Universities").click()
for i in df.index:
    entry = df.loc[i]
    try:
        adduni = browser.find_element(By.LINK_TEXT,"Add Universities").click()
        colgname=browser.find_element(By.NAME,"name")
        colgname.send_keys(entry.loc['Town'])
        time.sleep(2)
        try:
            colgname.submit()
        except StaleElementReferenceException:
            colgname=browser.find_element(By.NAME,"name")
            colgname.submit()
        time.sleep(3) 
    except StaleElementReferenceException:
        adduni = browser.find_element(By.LINK_TEXT,"Add Universities").click()
        colgname=browser.find_element(By.NAME,"name")
        colgname.send_keys(entry.loc['Town'])
        time.sleep(2)
        try:
            colgname.submit()
        except StaleElementReferenceException:
            colgname=browser.find_element(By.NAME,"name")
            colgname.submit()
        time.sleep(3) 
       
    
       

   