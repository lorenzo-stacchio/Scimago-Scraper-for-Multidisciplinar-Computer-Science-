import urllib.request
import pandas as pd
import os


def checkdircreate(path):
    if not os.path.exists(path):
        os.mkdir(path)


def download_url(url, path):
    folder_path = path  # f"outs/temp.csv"
    urllib.request.urlretrieve(url, folder_path)


def dataframe_update(temp_df, filter_area, filter_subareas):
    # Filter by area
    temp_df = temp_df[temp_df["Areas"].str.contains(filter_area)]
    # Filter by category
    for cat in filter_subareas:
        temp_df = temp_df[temp_df["Categories"].str.contains(cat)]

    return temp_df
    # temp_df.to_csv(f"{subfolder_path}{filter_area}_{contribution_name}.csv", index=False)
    # temp_df.to_excel(f"{subfolder_path}{filter_area}_{contribution_name}.xlsx", index=False)


pivot_area_code = "1700"  # computer science
pivot_sub_area_code = None  # eletrical and electronic engineering

# pivot_area_code = "2200"  # eletrical and electronic engineering
# pivot_sub_area_code = "2208"  # eletrical and electronic engineering

# pivot_code = "1400"
# pivot_code = "2000"
# filter_area = {"Economics, Econometrics and Finance":[], "Business, Management and Accounting":["Business and International Management", "Management Information Systems"]}
# filter_area = {"Economics, Econometrics and Finance":[], "Business, Management and Accounting":[]}
# filter_area = {"Arts and Humanities":["Visual Arts and Performing Arts"]}
# filter_area = {"Arts and Humanities":[""]}
# filter_area = {"Social Sciences":["Education", "E-learning"]}

filter_area = {"Engineering": ["Electrical and Electronic Engineering"],"Medicine": ["Health Informatics"]}

#filter_area = {"Medicine": ["Health Informatics"],"Computer Science": []}

list_types = ["j", "p"]


if __name__ == "__main__":
    path_csv_temp = f"outs/temp.csv"
    for contr_type in list_types:
        if pivot_sub_area_code:
            url_temp = f"https://www.scimagojr.com/journalrank.php?area={pivot_area_code}&category={pivot_sub_area_code}&type={contr_type}&out=xls"
        else:
            url_temp = f"https://www.scimagojr.com/journalrank.php?area={pivot_area_code}&type={contr_type}&out=xls"

        download_url(url_temp, path_csv_temp)
        temp_df = pd.read_csv(path_csv_temp, sep=";")
        suffix = ""
        for area, subarea in filter_area.items():
            temp_df = dataframe_update(
                temp_df=temp_df, filter_area=area, filter_subareas=subarea)
            suffix += f"{area}" + "_".join(subarea)
        
        # print(temp_df)
        # print(temp_df.columns)

        ## final format
        if pivot_sub_area_code:
            temp_df = temp_df[["Rank", "SJR", "Title", "SJR Quartile", "H index", "Publisher", "Areas", "Categories"]]
        else:
            temp_df = temp_df[["Rank", "SJR", "Title", "SJR Best Quartile",
                        "H index", "Publisher", "Areas", "Categories"]]
            
        temp_df["SJR"] = temp_df["SJR"].apply(
            lambda x: float(str(x).replace(",", ".")))
        # temp_df.to_csv(f"{subfolder_path}{filter_area}_{contribution_name}.csv", index=False)
        temp_df.to_csv(f"outs/temp_formatted_{suffix}_{contr_type}.csv")