import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl.styles import Font
from openpyxl.drawing.image import Image
from openpyxl.worksheet.hyperlink import Hyperlink

def clean_duplicate_spaces(text):
    # Replace multiple spaces with a single space
    cleaned_text = re.sub(r'\s+', ' ', text)
    # Remove leading and trailing spaces
    cleaned_text = cleaned_text.strip()
    return cleaned_text

def dataframe_to_excel_workbook(index_url_columns):
    # Create an Excel workbook and select the active worksheet
    wb = Workbook()
    ws = wb.active

    # Write the DataFrame to the worksheet
    for r_idx, row in enumerate(dataframe_to_rows(df, index=False, header=True), 1):
        for c_idx, value in enumerate(row, 1):
            cell = ws.cell(row=r_idx, column=c_idx, value=value)
            if r_idx > 1 and c_idx == index_url_columns:  # Assuming URLs are in the second column
                cell.hyperlink = value
                cell.style = 'Hyperlink'
    return wb
        
# URL of the page you want to scrape
url = 'https://cvpr.thecvf.com/Conferences/2024/AcceptedPapers'

keywords = ["Nerf", "Gaussian splatting", "Inpainting", "cultural", "3D generation", "fashion", "neural radiance",
            "human-centric", "video generation", "video synthesis", "pano", "personalized", "multimodal"]

keywords = [x.lower() for x in keywords]

# Send a GET request to the URL
response = requests.get(url)
papers, keywords_found, refs, authors = [], [], [], []

# Check if the request was successful
if response.status_code == 200:
    # Parse the page content
    soup = BeautifulSoup(response.content, 'html.parser')
    # print(soup)

    # Extract data (for example, all paragraphs)
    paragraphs = soup.find_all('td')

    # Print each paragraph's text
    for p in paragraphs:
        txt = p.get_text()
        txt = clean_duplicate_spaces(txt)
        txt = txt.replace("Arch 4A-E", "")
        txt = txt.replace("Exhibit Hall", "")
        paper_authors = txt.split("&")
        if len(paper_authors) == 2:
            paper, author = paper_authors
            paper_l = paper.lower()
            ks = [k for k in keywords if k in paper_l]
            # print(ks)
            if len(ks) > 0:
                # print(paper,"---",author)
                paper = paper.split("Poster Session")[0]
                papers.append(paper)
                keywords_found.append(",".join(ks))
                author = author.replace(" · ", ", ").strip()
                authors.append(author)
                # parse href if exist
                a_tags = p.find_all('a')
                if len(a_tags) > 0:
                    # for a in a_tags:
                    # Extract the href attribute
                    href = a_tags[0].get('href')
                    refs.append(href)
                else:
                    refs.append(None)
else:
    print(f"Failed to retrieve the page. Status code: {response.status_code}")


df = pd.DataFrame()

df["paper"] = papers
df["project_page"] = ["Yes" if ref else "No" for ref in refs]
df["url"] = refs
df["keywords"] = keywords_found
df["authors"] = authors

df.to_excel("scraperCVPR/text.xlsx", index=False)
df.to_csv("scraperCVPR/text.csv", index=False)

wb = dataframe_to_excel_workbook(index_url_columns=3)
# Save the workbook
wb.save("scraperCVPR/data_with_urls.xlsx")