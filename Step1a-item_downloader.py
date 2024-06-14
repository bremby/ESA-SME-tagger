#!/usr/bin/python3

# Gather a list of raw HTML entries straight from ESA's SME database. These shall be processed later.

import pdb
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
from bs4 import BeautifulSoup
import time

driver = webdriver.Firefox()
# Open the webpage
driver.get('https://esastar-emr.sso.esa.int/PublicEntityDir/PublicEntityDirSme')
# Wait for the page to load
wait = WebDriverWait(driver, 10)
wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'grid-row')))  # Adjust as needed

# Function to scroll to the bottom of the page
def scroll_to_bottom():
    driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
    time.sleep(0.5) 

def next_page():
    try:
        driver.find_element(By.XPATH, '//ul[@class="pagination"]/li[last()]/a').click();
        time.sleep(4)
        return True
    except Exception as e:
        eprint(e)
        return False


all_items = []

while True:
    # pdb.set_trace()

    # Parse the page content with BeautifulSoup
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    list_items = soup.find_all('tr', class_='grid-row')  # Adjust selector as needed

    all_items += list_items
    scroll_to_bottom()
    if not next_page():
        break

print(all_items)

# Close the WebDriver
driver.quit()
