from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
import pickle, os, json, ast

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


# Set up Chrome options
chrome_options = Options()
# Path to the Chrome WebDriver executable

# Start the WebDriver
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install(),chrome_options=chrome_options))


url = "https://www.scimagojr.com"

driver.get(url)
time.sleep(10)

if os.path.exists("cookies.txt"):
    # Deserialize the cookie from the file
    cookies = get_cookies("cookies.txt")
    for c in cookies: 
        try:
            driver.add_cookie(c)
        except Exception as e:
            print(e)
    # cookie = pickle.load(f)
    print("Cookie loaded")  

driver.get(url)

# Wait for the page to load
time.sleep(20)