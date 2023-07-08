from selenium import webdriver
import numpy as np

import time
from selenium import webdriver

from selenium.webdriver.common.by import By
#from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located
import re
from selenium.webdriver import Keys, ActionChains
from selenium.common.exceptions import ElementClickInterceptedException
import pyautogui
import warnings
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import pandas as pd
from selenium.webdriver.support import expected_conditions as EC

import re
from selenium.webdriver import Keys, ActionChains

from selenium.common.exceptions import ElementClickInterceptedException

import pyautogui
import warnings
warnings.filterwarnings("ignore")

import re
from selenium.webdriver import Keys, ActionChains

from selenium.common.exceptions import ElementClickInterceptedException

import pyautogui
import warnings



options = webdriver.ChromeOptions()
prefs = {"profile.default_content_setting_values.notifications" : 2}
options.add_experimental_option("prefs",prefs)
options.page_load_strategy = 'eager'
service = Service(executable_path="chromedriver.exe")
driver = webdriver.Chrome(service=service, options=options)

#DesiredCapabilities.CHROME = None

driver.maximize_window()

driver.get("https://www.eldorado.ru/d/kompyuternye-komplektuyushchie/")
WebDriverWait(driver, 10).until(expected_conditions.visibility_of_element_located((By.XPATH, '/html/body/div[2]/div[1]/main/div/div/div[4]/div[2]/a[1]/span[2]')))
driver.find_element(By.XPATH, '/html/body/div[2]/div[1]/main/div/div/div[4]/div[2]/a[1]/span[2]').click


if "Access to resource was blocked." == driver.find_element(By.XPATH, '/html/body').text.split('\n')[0]:
    driver.get("https://www.eldorado.ru/d/kompyuternye-komplektuyushchie/")            
    try:
        element = driver.find_element(By.XPATH, '/html/body/div[4]')
        driver.execute_script("arguments[0].remove();", element)
    except Exception:
        pass

#driver.back()
try: 
    WebDriverWait(driver, 10).until(expected_conditions.visibility_of_element_located((By.XPATH, '/html/body/div[2]/div[1]/main/div/div/div[3]/div[2]/a[1]/span[2]')))
    driver.find_element(By.XPATH, '/html/body/div[2]/div[1]/main/div/div/div[3]/div[2]/a[1]').click()
except ElementClickInterceptedException:
    pass

data_link = pd.read_csv('./data/eldorado/cpu/link.csv')
link = dict()
start_page = 1
start_card = 1
number_of_reviews = (start_page - 1) * 34


for num in range (start_page, 15):
    time.sleep(2)
    print("num = ", num)
    for i in range(start_card, 37):
        #print("i = ", i)
        #time.sleep(2)
        #   Переход на страницу товара
        try: 
            #WebDriverWait(driver, 10).until(expected_conditions.visibility_of_element_located((By.XPATH, f'/html/body/div[2]/div[1]/main/div/div/div[7]/div[2]/div[1]/ul/li[{i}]/div[2]/a')))
            search_box = driver.find_element(By.XPATH, f'/html/body/div[2]/div[1]/main/div/div/div[7]/div[2]/div[1]/ul/li[{i}]/div[2]/a')
            #print(search_box.get_attribute("href"))     
            #print("1!")
        except Exception as e:
            pass
            #print("1)")
        try:                                            
            #WebDriverWait(driver, 10).until(expected_conditions.visibility_of_element_located((By.XPATH, f'/html/body/div[2]/div[1]/main/div/div/div[8]/div[2]/div[1]/ul/li[{i}]/div[2]/a')))
            search_box = driver.find_element(By.XPATH, f'/html/body/div[2]/div[1]/main/div/div/div[8]/div[2]/div[1]/ul/li[{i}]/div[2]/a')
            #print("2!")
        except Exception as e:
            pass

        if "Access to resource was blocked." == driver.find_element(By.XPATH, '/html/body').text.split('\n')[0]:

            
            driver.get("https://www.eldorado.ru/d/kompyuternye-komplektuyushchie/")            
            try:
                element = driver.find_element(By.XPATH, '/html/body/div[4]')
                driver.execute_script("arguments[0].remove();", element)
            except Exception:
                pass
            try: 
                time.sleep(3)
                driver.find_element(By.XPATH, '/html/body/div[2]/div[1]/main/div/div/div[4]/div[2]/a[1]/span[1]').click
            except Exception:
                continue
            for j in range(1, num):
                if "Access to resource was blocked." == driver.find_element(By.XPATH, '/html/body').text.split('\n')[0]:
                    continue
                else:
                    try:
                        WebDriverWait(driver, 10).until(expected_conditions.visibility_of_element_located((By.CLASS_NAME, 'next')))
                        driver.find_element(By.CLASS_NAME, 'next').click()
                    except Exception:
                        if "Access to resource was blocked." == driver.find_element(By.XPATH, '/html/body').text.split('\n')[0]:
                            continue

        link.update({'link': search_box.get_attribute("href")})                         
        data_link = data_link.append(link, ignore_index=True) 
        data_link.to_csv(f'./data/eldorado/cpu/link.csv', index=False)

        try:
            try:
                element = driver.find_element(By.XPATH, '/html/body/div[4]')
                driver.execute_script("arguments[0].remove();", element)
            except Exception:
                pass
        except Exception:
            pass

        link.clear()
    start_card = 1
    WebDriverWait(driver, 10).until(expected_conditions.visibility_of_element_located((By.CLASS_NAME, 'next')))
    driver.find_element(By.CLASS_NAME, 'next').click()


