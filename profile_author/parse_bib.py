import bibtexparser
import pandas as pd
import requests
import os
import Levenshtein
import tqdm

# Function to read a .bib file and parse its content


def parse_biblatex_file(file_path):
    with open(file_path, 'r') as bib_file:
        bib_database = bibtexparser.load(bib_file)
    return bib_database


def get_journal_csv(year, path):
    url = f"https://www.scimagojr.com/journalrank.php?area=1700&year={year}&out=xls"
    # Send an HTTP GET request to the URL
    response = requests.get(url)
    out_path = f'{path}/{year}.csv'
    if not os.path.exists(out_path):
        # Check if the request was successful
        if response.status_code == 200:
            # Open a file in binary write mode
            with open(out_path, 'wb') as file:
                # Write the content of the response (which is the .xlsx file) to the file
                file.write(response.content)
            print('File downloaded successfully.')
        else:
            print(
                f'Failed to download file. HTTP Status Code: {response.status_code}')
    return pd.read_csv(out_path, sep=";")


def get_quartile(name, year):
    df_journal = get_journal_csv(year, scimago_folder)
    best_match = ""        
    min_distance = float("inf")
    for idx, row in df_journal.iterrows():
        # print(row["Title"])
        d = Levenshtein.distance(row["Title"], name)
        if d < min_distance:
            best_match = row["SJR Best Quartile"]
            min_distance = d
    return best_match

# Example usage
file_path = 'profile_author\stacchio.bib'
bib_database = parse_biblatex_file(file_path)


df_recap = pd.DataFrame(
    columns=["Title", "Type", "JCName", "Quartile", "Year"])
scimago_folder = "profile_author\\scimago\\"

# Access entries
entries = bib_database.entries

author_name = "Lorenzo Stacchio"

for entry in tqdm.tqdm(entries, total=len(entries)):
    title = entry["title"]
    Type = entry["ENTRYTYPE"]
    year = entry["year"]
    if Type == "article":
        JCName = entry["journal"]
        quartile = get_quartile(JCName,year)

    else:
        JCName = entry["booktitle"]
        quartile = ""

    # print(entry["ENTRYTYPE"])
    df_recap = df_recap._append({"Title": title, "Type": Type, "JCName": JCName,
                                "Quartile": quartile, "Year": year}, ignore_index=True)

df_recap.to_excel(f"profile_author\\{author_name}.xlsx")
