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
    button_element = driver.find_element(By.XPATH, button_xpath)
    button_element.click()

def check_SSID(driver, url, ssids):
    driver.get(url)
    time.sleep(1)
    path_categories ="//div[@class='journalgrid']//div[@style='height: auto !important;']//ul//li//a"
    el = None
    while not el:
        el = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, path_categories)))
    rows = driver.find_elements(By.XPATH, path_categories)
    rows = [r.get_attribute("href").split("=")[1] for r in rows]
    truthness = any([ssid in rows for ssid in ssids])
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
            good_items[href] = tuple(row_data[1:4])
    ## Map compatible journals
    good_items = [v for k,v in good_items.items() if check_SSID(driver,k,ssids)]
    return good_items

def get_pagination(driver):
    pagination = "//div[@class='half_block']//div[@class='pagination']"
    # button class="fc-button fc-cta-consent fc-primary-button" role="button" aria-label="Acconsento" tabindex="0"><div class="fc-button-background"></div><p class="fc-button-label">Acconsento</p></button>    
    num = driver.find_element(By.XPATH, pagination).text
    num = num.split(" ")[-1]
    return int(num) 

pivot_code = "1700"
list_search = ["1211,1702"]
list_types = ["j"]

if __name__=="__main__":
    # Set up Chrome options
    chrome_options = Options()
    # Path to the Chrome WebDriver executable
    # chrome_options.add_argument('--headless')
    good_items_dict = {}
    items_per_page = 50
    # Start the WebDriver
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),options=chrome_options)
    url = "https://www.scimagojr.com"

    driver.get(url)
    time.sleep(1)

    if os.path.exists("cookies.txt"):
        # Deserialize the cookie from the file
        cookies = get_cookies("cookies.txt")
        for c in cookies: 
            try:
                driver.add_cookie(c)
            except Exception as e:
                print(e)
        print("Cookie loaded")  
    time.sleep(1)
    for contr_type in list_types:
        good_items_dict[contr_type] = []
        url_temp = f"https://www.scimagojr.com/journalrank.php?area={pivot_code}&type={contr_type}"
        driver.get(url_temp)
        time.sleep(2)
        click_cookie(driver)
        total_rows = get_pagination(driver)
        pages = (total_rows//items_per_page) + (total_rows%items_per_page != 0)
        # tqdm.tqdm(good_items.items(), total = len(good_items)) 
        for pageidx in tqdm.tqdm(range(1,pages), total = pages):
            url_temp = f"https://www.scimagojr.com/journalrank.php?area={pivot_code}&type={contr_type}&page={pageidx}&total_size={total_rows}"
            driver.get(url_temp)
            time.sleep(2)
            good_items_dict[contr_type].extend(parse_page(driver=driver,ssids=list_search))
            print(f"Found items {len(good_items_dict)}")
    # Wait for the page to load
    time.sleep(30)