import pandas as pd
import Levenshtein

def nearest_levesthein(title, df):
    min_str = ""
    min_poster = ""
    min_distance = float("inf")
    for idx, row in df.iterrows():
        d = Levenshtein.distance(title,row["paper"])
        if d < min_distance:
            min_str = row["paper"]
            min_poster = row["poster_session"]
            min_distance = d
    return min_str, min_poster

df = pd.read_csv("scraperCVPR/text.csv")

df_titles = pd.read_csv("scraperCVPR/data_with_urls.xlsx - Final List.csv")


df_titles_panels = []


for idx, row in df_titles.iterrows():
    paper_title = row["paper"]
    best, poster = nearest_levesthein(paper_title,df)
    # print(paper_title,best, "\n\n\n")
    df_titles_panels.append(poster)

df_titles["poster"] = df_titles_panels


df_titles.to_csv("scraperCVPR/data_with_urls.xlsx - reduced_TITLES.csv", index=False)
df_titles.to_excel("scraperCVPR/data_with_urls.xlsx - reduced_TITLES.xlsx", index=False)

