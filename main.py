from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
import pickle, os, json, ast
import tqdm
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import urllib.request 
import pandas as pd

def get_cookies(path: str) -> dict:
    """
    Gets cookies from the passed file using the netscape standard
    """
    with open(path, 'r', encoding='utf-8') as file:
        lines = file.read().split('\n')

    return_cookies = []
    for line in lines:
        split = line.split('\t')
        if len(split) < 6:
            continue

        split = [x.strip() for x in split]
        if "scimago" in split[0]:
            try:
                split[4] = int(split[4])
            except ValueError:
                split[4] = None

            return_cookies.append({
                'name': split[5],
                'value': split[6],
                # 'domain': split[0],
                # 'path': split[2],
            })

            if split[4]:
                return_cookies[-1]['expiry'] = split[4]
    return return_cookies  


def click_cookie(driver):
    button_xpath = "//button[@class='fc-button fc-cta-consent fc-primary-button']"
    # button class="fc-button fc-cta-consent fc-primary-button" role="button" aria-label="Acconsento" tabindex="0"><div class="fc-button-background"></div><p class="fc-button-label">Acconsento</p></button>    
    try: 
        button_element = driver.find_element(By.XPATH, button_xpath)
        button_element.click()
    except Exception as e:
        pass

def check_SSID(driver, url, ssids):
    driver.get(url)
    time.sleep(1)
    path_categories ="//div[@class='journalgrid']//div[@style='height: auto !important;']//ul//li//a"
    # el = None
    # while not el:
    #     try:
    #         el = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, path_categories)))
    #     except Exception as e:
    #         pass
    time.sleep(1)
    rows = driver.find_elements(By.XPATH, path_categories)
    rows = [r.get_attribute("href").split("=")[1] for r in rows]
    truthness = [ssid for ssid in ssids if ssid in rows]
    return truthness

def parse_page(driver, ssids):
    table_xpath = "//div[@class='table_wrap']//tbody//tr"
    # button class="fc-button fc-cta-consent fc-primary-button" role="button" aria-label="Acconsento" tabindex="0"><div class="fc-button-background"></div><p class="fc-button-label">Acconsento</p></button>    
    rows = driver.find_elements(By.XPATH, table_xpath)
    good_items = {}
    # good_items["https://www.scimagojr.com/journalsearch.php?q=23616&tip=sid&clean=0"] = ["test"]

    for row in rows:
        # Example: Extracting text from each cell in the row
        cells = row.find_elements(By.TAG_NAME, "td")
        row_data = [cell.text for cell in cells]
        href = cells[1].find_element(By.TAG_NAME, "a").get_attribute("href")
        if "Q1" in row_data[3]:
            # check scientific sectors
            good_items[href] = row_data[1:4]
    ## Map compatible journals
    # toret = []
    # for k,v in tqdm.tqdm(good_items.items(), total=len(good_items), desc="Parsing page"):
    #     cat = check_SSID(driver,k,ssids)
    #     if len(cat)>0:
    #         v.append(cat)
    #         toret.append(v)
    return good_items


def download_url_and_dataframe_update(url, filter_category, contribution_name):
    urllib.request.urlretrieve(url, "test.csv")
    temp_df = pd.read_csv("test.csv", sep=";")
    filtered = temp_df["Categories"].str.contains(filter_category)
    temp_df = temp_df[filtered]
    temp_df = temp_df[["Rank","Title","H index","Publisher","Categories"]]
    temp_df.to_csv(f"{filter_category}_{contribution_name}.csv", index=False)
    temp_df.to_excel(f"{filter_category}_{contribution_name}.xlsx", index=False)


def get_pagination(driver):
    pagination = "//div[@class='half_block']//div[@class='pagination']"
    # button class="fc-button fc-cta-consent fc-primary-button" role="button" aria-label="Acconsento" tabindex="0"><div class="fc-button-background"></div><p class="fc-button-label">Acconsento</p></button>    
    num = driver.find_element(By.XPATH, pagination).text
    num = num.split(" ")[-1]
    return int(num) 

pivot_code = "1700"
filter_cat = ["Philosophy"]
list_types = ["j", "p"]


if __name__=="__main__":
    for contr_type in list_types:
        for cat in filter_cat:
            url_temp = f"https://www.scimagojr.com/journalrank.php?area={pivot_code}&type={contr_type}&out=xls"
            download_url_and_dataframe_update(url=url_temp, filter_category=cat, contribution_name=contr_type)