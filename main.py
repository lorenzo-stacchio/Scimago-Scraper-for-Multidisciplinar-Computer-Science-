import urllib.request 
import pandas as pd


def download_url_and_dataframe_update(url, filter_area,filter_subareas,contribution_name):
    urllib.request.urlretrieve(url, f"test_{contribution_name}.csv")
    temp_df = pd.read_csv(f"test_{contribution_name}.csv", sep=";")
    ## Filter by area
    temp_df = temp_df[temp_df["Areas"].str.contains(filter_area)]
    ## Filter by category
    for cat in filter_subareas:
        temp_df = temp_df[temp_df["Categories"].str.contains(cat)]

    temp_df = temp_df[["Rank","SJR","Title","H index","Publisher","Areas", "Categories"]]
    temp_df["SJR"] = temp_df["SJR"].apply(lambda x: float(str(x).replace(",",".")))
    temp_df.to_csv(f"{filter_area}_{contribution_name}.csv", index=False)
    temp_df.to_excel(f"{filter_area}_{contribution_name}.xlsx", index=False)


pivot_code = "1700" # computer scienc
filter_area = {"Economics, Econometrics and Finance":[], "Business, Management and Accounting":["Business and International Management", "Management Information Systems"]}
list_types = ["j"] #, "p"]


if __name__=="__main__":
    for contr_type in list_types:
        for area, subarea in filter_area.items():
            url_temp = f"https://www.scimagojr.com/journalrank.php?area={pivot_code}&type={contr_type}&out=xls"
            download_url_and_dataframe_update(url=url_temp, filter_area=area, filter_subareas =subarea, contribution_name=contr_type)