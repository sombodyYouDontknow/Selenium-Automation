from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import pandas as pd
import time

df = pd.read_excel('colg_urls.xlsx')

s = Service("C:/chromedriver/chromedriver")
drivers = webdriver.Chrome(service=s)

drivers.get("https://www.google.com/")


def click(driver, locator):
    try:
        WebDriverWait(driver, 30).until(ec.presence_of_element_located(locator)).click()
    except ec:
        WebDriverWait(driver, 20).until(ec.frame_to_be_available_and_switch_to_it(locator)).click()


def send_Keys(driver, locator, value):
    try:
        WebDriverWait(driver, 30).until(ec.presence_of_element_located(locator)).send_keys(value)
    except ec:
        WebDriverWait(driver, 7).until(ec.alert_is_present())
        alert = driver.switch_to.alert
        alert.accept()
        WebDriverWait(driver, 30).until(ec.presence_of_element_located(locator)).send_keys(value)


def Submit(driver, locator):
    try:
        WebDriverWait(driver, 30).until(ec.presence_of_element_located(locator)).submit()
    except ec:
        WebDriverWait(driver, 7).until(ec.alert_is_present())
        alert = driver.switch_to.alert
        alert.accept()
        WebDriverWait(driver, 30).until(ec.presence_of_element_located(locator)).submit()


def clear_text(driver, locator):
    try:
        WebDriverWait(driver, 30).until(ec.presence_of_element_located(locator)).clear()
    except ec:
        WebDriverWait(driver, 20).until(ec.frame_to_be_available_and_switch_to_it(locator)).click()


for i in df.index:
    entry = df.loc[i]
    click(drivers, (By.NAME, "q"))
    time.sleep(1)
    send_Keys(drivers, (By.NAME, "q"), entry["NAME"])
    time.sleep(1)
    Submit(drivers, (By.NAME, "q"))
    time.sleep(1)
    click(drivers, (By.CSS_SELECTOR, "h3.LC20lb"))
    urls = drivers.current_url
    f = open("urls.txt", "a")
    f.write("\n " + urls)
    f.close()
    print(urls)
    drivers.back()
    time.sleep(1)
    clear_text(drivers, (By.NAME, "q"))
