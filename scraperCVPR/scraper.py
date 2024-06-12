import requests
from bs4 import BeautifulSoup
import re
import pandas as pd 

def clean_duplicate_spaces(text):
    # Replace multiple spaces with a single space
    cleaned_text = re.sub(r'\s+', ' ', text)
    # Remove leading and trailing spaces
    cleaned_text = cleaned_text.strip()
    return cleaned_text

# URL of the page you want to scrape
url = 'https://cvpr.thecvf.com/Conferences/2024/AcceptedPapers'

keywords = ["Nerf", "Gaussian splatting", "Inpainting", "cultural", "3D generation","fashion",
            "human-centric","video generation","video synthesis", "pano","personalized", "multimodal"]

keywords = [x.lower() for x in keywords]

# Send a GET request to the URL
response = requests.get(url)
papers, keywords_found, authors = [],[],[]

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
        txt = txt.replace("Arch 4A-E","")
        txt = txt.replace("Exhibit Hall","")
        paper_authors = txt.split("&")
        if len(paper_authors) == 2:
            paper,author = paper_authors
            paper_l = paper.lower()
            ks = [k for k in keywords if k in paper_l]
            # print(ks)
            if len(ks) > 0:
                # print(paper,"---",author)
                paper = paper.split("Poster Session")[0]
                papers.append(paper)
                keywords_found.append(",".join(ks))
                author = author.replace(" · ",", ").strip()
                authors.append(author)
else:
    print(f"Failed to retrieve the page. Status code: {response.status_code}")


df = pd.DataFrame(columns = ["paper","keywords","authors"])

df["paper"] = papers
df["keywords"] = keywords_found
df["authors"] = authors

df.to_excel("scraperCVPR/text.xlsx", index=False)