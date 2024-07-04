import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl.styles import Font
from openpyxl.drawing.image import Image
from openpyxl.worksheet.hyperlink import Hyperlink
import Levenshtein

base_url = "https://www.scimagojr.com/"
base_journal = "https://www.scimagojr.com/journalsearch.php?q="

df_recap = pd.read_excel("profile_author\\author_recap.xlsx")

for idx,row in df_recap.iterrows():
    year = row["year"]
    if row["Type"] == "article":
        response = requests.get(base_journal + row["JCName"])
        soup = BeautifulSoup(response.content, 'html.parser')

        response_links = soup.find_all('a',href=True)
        min_distance = float("inf")
        best_match = ""
        for tag in response_links:
            if "journalsearch" in tag["href"] and tag.text != "":
                # print(tag)
                name = str(tag).split("</span>")[0] 
                name = name.split("<span class=\"jrnlname\">")[1]
                d = Levenshtein.distance(row["JCName"], name)
                # print(row["JCName"], name,d)
                # print("\n\n\n\n")
                if d < min_distance:
                    best_match = f"{base_url}{tag['href']}"
                    min_distance = d
                
        print(best_match)
        
        ### SCRAPE PAGE JOURNAL
        
