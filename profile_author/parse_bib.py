import bibtexparser
import pandas as pd
import requests
import os
import Levenshtein
import tqdm

# Function to read a .bib file and parse its content


def parse_biblatex_file(file_path):
    with open(file_path, 'r', encoding="utf-8") as bib_file:
        bib_database = bibtexparser.load(bib_file)
    return bib_database


def get_conference_csv(year, path):
    url_core_export_all = "https://portal.core.edu.au/conf-ranks/?search=&by=all&source=all&sort=atitle&page=1&do=Export"
    # response = requests.get(url_core_export_all)
    out_path = f'{path}/CORE_complete.csv'
    download_file_csv(url_core_export_all, out_path)

    # core_index = [2008, 2010, 2013, 2014, 2017, 2018, 2020, 2021, 2023]
    # # era_index = [2010]
    # sel_year = None
    # sel_year_name = ""
    # for start, end in range(0, core_index-1):
    #     if year == start:
    #         sel_year = core_index[start]
    #         break
    #     elif year > start and year <= end:
    #         sel_year = core_index[end]
    #         break
    # print(sel_year)
    # if sel_year == 2010:
    #     sel_year_name = f"ERA{sel_year}"
    # else:
    #     sel_year_name = f"CORE{sel_year}"

    # print(sel_year_name)
    df = pd.read_csv(out_path)
    # print(df.columns)
    df.columns = ['index','Title', 'acr', 'ranking', "rank","boolean" ,"primary for", "comments", "average rating"]
    # df = df.reset_index()
    # print(df.columns)
    return df


def download_file_csv(url, out_path):
    if not os.path.exists(out_path):
        response = requests.get(url)
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


def get_journal_csv(year, path):
    url = f"https://www.scimagojr.com/journalrank.php?area=1700&year={year}&out=xls"
    # Send an HTTP GET request to the URL
    out_path = f'{path}/{year}.csv'
    download_file_csv(url, out_path)
    return pd.read_csv(out_path, sep=";")


def get_quartile(name, year, type_pub, threshold=10):
    if type_pub == "article":
        df_journal = get_journal_csv(year, scimago_folder)
        best_match = ""
        best_url = ""
        min_distance = float("inf")
        # print("\nJOURNAL NAME", name)
        for idx, row in df_journal.iterrows():
            d = Levenshtein.distance(row["Title"].lower(), name.lower())
            # if "sensors" in row["Title"].lower():
            #     print(row["Title"].lower())
            #     print(name, d)
            # threshold guarantees that non correct or similar name journals are not matched
            if d < threshold and d < min_distance:
                best_match = row["SJR Best Quartile"]
                min_distance = d
    else:  # in proceedings
        df_conference = get_conference_csv(year, scimago_folder)
        best_match = ""
        best_url = ""
        min_distance = float("inf")
        # print("\CONFERENCE NAME", name)
        for idx, row in df_conference.iterrows():
            d = Levenshtein.distance(row["Title"].lower(), name.lower())
            # threshold guarantees that non correct or similar name journals are not matched
            if d < threshold and d < min_distance:
                best_match = row["rank"]
                min_distance = d
    return best_match

# Example usage


df_recap = pd.DataFrame(
    columns=["Title", "Type", "JCName", "Quartile", "Year"])
scimago_folder = "profile_author\\scimago\\"

# Access entries
# author_name = "Pasquale Cascarano"
# file_path = 'profile_author\cascarano.bib'
# file_path = 'profile_author\pietrini.bib'
file_path = 'profile_author\\stacchio.bib'

# file_path = 'profile_author\stacchio.bib'
author_name = os.path.basename(file_path).split(".")[0]  # "Lorenzo Stacchio"
bib_database = parse_biblatex_file(file_path)
entries = bib_database.entries


for entry in tqdm.tqdm(entries, total=len(entries)):
    try:
        title = entry["title"]
        Type = entry["ENTRYTYPE"]
        year = entry["year"]
        if Type == "article":
            JCName = entry["journal"]
            if JCName == "Sensors":
                print(JCName)
            quartile = get_quartile(JCName, year, type_pub=Type)
            if quartile == "" or quartile == "-":  # do not match computer science
                continue
            print("\nJOURNAL NAME", JCName, quartile)

        else:
            JCName = entry["booktitle"]
            quartile = get_quartile(JCName, year, type_pub=Type, threshold=5)
            print("\CONFERENCE NAME",JCName, quartile)
            if quartile == "" or quartile == "Unranked":  # do not match computer science
                quartile = "NOTCORE"
        # print(entry["ENTRYTYPE"])
        df_recap = df_recap._append({"Title": title, "Type": Type, "JCName": JCName,
                                    "Quartile": quartile, "Year": year}, ignore_index=True)
    except Exception as e:
        # print("Error: ", e)
        pass

df_recap.to_excel(f"profile_author\\{author_name}.xlsx", index=False)

print(df_recap.Quartile.value_counts())
