from lib2to3.pgen2 import driver
import selenium
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.select import Select
from config import Usernmae, Password,Link
import pandas as pd
import time

df = pd.read_excel('district.xlsx')
driver_service = Service(executable_path="C:\chromedriver2\chromedriver")
drivers = webdriver.Chrome(service=driver_service)

drivers.get(Link)
time.sleep(2)


def click(driver, locator):
    WebDriverWait(driver, 10).until(ec.presence_of_element_located(locator)).click()


def send_Keys(driver, locator, value):
    WebDriverWait(driver, 10).until(ec.presence_of_element_located(locator)).send_keys(value)


def Submit(driver, locator):
    WebDriverWait(driver, 10).until(ec.presence_of_element_located(locator)).submit()


def select_item(driver, locator, value):
    item = WebDriverWait(driver, 10).until(ec.presence_of_element_located(locator))
    Select(item).select_by_value(value)


click(drivers, (By.ID, "email"))
send_Keys(drivers, (By.ID, "email"), Usernmae)

click(driver, (By.ID, "password"))
send_Keys(drivers, (By.ID, "password"), Password)

Submit(drivers, (By.NAME, "btnLogin"))

drivers.implicitly_wait(30)

click(drivers, (By.LINK_TEXT, "Districts"))
click(drivers, (By.LINK_TEXT, "Add Districts"))

for i in df.index:
    entry = df.loc[i]
    click(driver, (By.LINK_TEXT, "Add Districts"))
    select_item(driver, (By.NAME, "state_id"), "5")
    click(driver, (By.NAME, "name"))
    send_Keys(driver, (By.NAME, "name"), entry["district"])
    time.sleep(2)
    Submit(driver, (By.CLASS_NAME, "btn-success"))
