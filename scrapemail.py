import self as self
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
import pandas as pd
import time
import re
import csv

from selenium.webdriver.support.wait import WebDriverWait

df = pd.read_excel('urls.xlsx')
opt = webdriver.ChromeOptions()
opt.add_argument('--no-sandbox')
opt.add_argument('--disable-gpu')
opt.add_argument('--disable-software-pasteurizer')
opt.add_argument('--disable-dev-shm-usage')
s = Service('C:/chromedriver/chromedriver')
drivers = webdriver.Chrome(service=s, options=opt)

drivers.get('https://www.google.com/')


def Get_email(source):
    EMAIL_REGEX = r'''(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])'''
    email = re.finditer(EMAIL_REGEX, source)
    return email


def Get_phone(source):
    PHONE_REGEX = r'''[0-9]{4,5}\s[0-9]{6}........................|[0-9]{5}\s[0-9]{5}|[0-9]{4,5}-[0-9]{6}'''
    phone = re.finditer(PHONE_REGEX, source)
    return phone


def Get_element(locator):
    drivers.find_element(By.PARTIAL_LINK_TEXT, locator)


def click(driver, locator):
    try:
        WebDriverWait(driver, 40).until(ec.presence_of_element_located(locator)).click()
    except NoSuchElementException:
        WebDriverWait(driver, 40).until(ec.element_to_be_clickable(locator)).click()
        WebDriverWait(driver, 40).until(ec.frame_to_be_available_and_switch_to_it(locator)).click()


def send_Keys(driver, locator, value):
    try:
        WebDriverWait(driver, 40).until(ec.presence_of_element_located(locator)).send_keys(value)
    except ec:
        WebDriverWait(driver, 7).until(ec.alert_is_present())
        alert = driver.switch_to.alert
        alert.accept()
        WebDriverWait(driver, 40).until(ec.frame_to_be_available_and_switch_to_it(locator)).send_keys(value)


def Submit(driver, locator):
    try:
        WebDriverWait(driver, 40).until(ec.presence_of_element_located(locator)).submit()
    except ec:
        WebDriverWait(driver, 7).until(ec.alert_is_present())
        alert = driver.switch_to.alert
        alert.accept()
        WebDriverWait(driver, 40).until(ec.presence_of_element_located(locator)).submit()


def clear_text(driver, locator):
    try:
        WebDriverWait(driver, 40).until(ec.presence_of_element_located(locator)).clear()
    except ec:
        WebDriverWait(driver, 20).until(ec.frame_to_be_available_and_switch_to_it(locator)).click()


def DriverBack(driver):
    try:
        driver.back()
    except ec:
        WebDriverWait(driver, 40).until(ec.frame_to_be_available_and_switch_to_it(driver)).back()


for i in df.index:
    entry = df.loc[i]
    click(drivers, (By.NAME, "q"))
    time.sleep(1)
    name = entry['Name']
    url = entry['URLS']
    time.sleep(2)
    send_Keys(drivers, (By.NAME, 'q'), name)
    Submit(drivers, (By.NAME, "q"))
    drivers.implicitly_wait(2)
    try:
        Get_element('Contact')
        click(drivers, (By.PARTIAL_LINK_TEXT, 'Contact'))
    except NoSuchElementException:
        print('not present ')
        clear_text(drivers, (By.NAME, "q"))
        click(drivers, (By.NAME, "q"))
        send_Keys(drivers, (By.NAME, 'q'), url)
        time.sleep(2)
        Submit(drivers, (By.NAME, "q"))
        time.sleep(3)
        click(drivers, (By.CSS_SELECTOR, "h3.LC20lb"))
    Source_code = drivers.page_source
    time.sleep(3)
    emails = Get_email(Source_code)
    phones = Get_phone(Source_code)
    email_list = []
    phone_list = []
    data = {'Name': '', 'Email': '', 'Phone': ''}

    for re_match in phones:
        phone_list.append(re_match.group())

    for re_match in emails:
        email_list.append(re_match.group())

    for email in email_list:
        data['Name'] = name
        data['Email'] = email

    for phone in phone_list:
        data['Phone'] = phone

    with open('organization_info.csv', 'a') as f:
        writer = csv.DictWriter(f, fieldnames=data.keys())
        writer.writerow(data)
    print(data)
    DriverBack(drivers)
    time.sleep(2)
    clear_text(drivers, (By.NAME, "q"))
