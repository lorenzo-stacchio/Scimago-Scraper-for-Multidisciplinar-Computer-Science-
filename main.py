import urllib.request 
import pandas as pd
import os 

def checkdircreate(path):
    if not os.path.exists(path):
        os.mkdir(path)
        

def download_url_and_dataframe_update(url, filter_area, filter_subareas,contribution_name):
    folder_path = f"outs/{filter_area}/"
    checkdircreate(folder_path)
    merged = "_".join(filter_subareas)
    subfolder_path = f"{folder_path}{merged}/"
    checkdircreate(subfolder_path)

    csv_temp_path = f"{subfolder_path}test_{contribution_name}.csv"
    urllib.request.urlretrieve(url, csv_temp_path)
    temp_df = pd.read_csv(csv_temp_path, sep=";")
    
    ## Filter by area
    temp_df = temp_df[temp_df["Areas"].str.contains(filter_area)]
    ## Filter by category
    for cat in filter_subareas:
        temp_df = temp_df[temp_df["Categories"].str.contains(cat)]

    temp_df = temp_df[["Rank","SJR","Title","SJR Best Quartile","H index","Publisher","Areas", "Categories"]]
    temp_df["SJR"] = temp_df["SJR"].apply(lambda x: float(str(x).replace(",",".")))
    temp_df.to_csv(f"{subfolder_path}{filter_area}_{contribution_name}.csv", index=False)
    temp_df.to_excel(f"{subfolder_path}{filter_area}_{contribution_name}.xlsx", index=False)


pivot_code = "1700" # computer science
# pivot_code = "1400"
# pivot_code = "2000"
# filter_area = {"Economics, Econometrics and Finance":[], "Business, Management and Accounting":["Business and International Management", "Management Information Systems"]}
# filter_area = {"Economics, Econometrics and Finance":[], "Business, Management and Accounting":[]}
# filter_area = {"Arts and Humanities":["Visual Arts and Performing Arts"]}
# filter_area = {"Arts and Humanities":[""]}
# filter_area = {"Social Sciences":["Education", "E-learning"]}
# filter_area = {"Engineering":["Electrical and Electronic Engineering"]}

filter_area = {"Environmental Science": []}

list_types = ["j", "p"]


if __name__=="__main__":
    for contr_type in list_types:
        for area, subarea in filter_area.items():
            url_temp = f"https://www.scimagojr.com/journalrank.php?area={pivot_code}&type={contr_type}&out=xls"
            print(url_temp)
            download_url_and_dataframe_update(url=url_temp, filter_area=area, filter_subareas =subarea, contribution_name=contr_type)