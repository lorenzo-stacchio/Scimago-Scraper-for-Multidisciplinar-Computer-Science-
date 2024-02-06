import urllib.request 
import pandas as pd


def download_url_and_dataframe_update(url, filter_category, contribution_name):
    urllib.request.urlretrieve(url, "test.csv")
    temp_df = pd.read_csv("test.csv", sep=";")
    filtered = temp_df["Categories"].str.contains(filter_category)
    temp_df = temp_df[filtered]
    temp_df = temp_df[["Rank","Title","H index","Publisher","Categories"]]
    temp_df.to_csv(f"{filter_category}_{contribution_name}.csv", index=False)
    temp_df.to_excel(f"{filter_category}_{contribution_name}.xlsx", index=False)


def get_pagination(driver):
    pagination = "//div[@class='half_block']//div[@class='pagination']"
    # button class="fc-button fc-cta-consent fc-primary-button" role="button" aria-label="Acconsento" tabindex="0"><div class="fc-button-background"></div><p class="fc-button-label">Acconsento</p></button>    
    num = driver.find_element(By.XPATH, pagination).text
    num = num.split(" ")[-1]
    return int(num) 

pivot_code = "1700"
filter_cat = ["Philosophy"]
list_types = ["j", "p"]


if __name__=="__main__":
    for contr_type in list_types:
        for cat in filter_cat:
            url_temp = f"https://www.scimagojr.com/journalrank.php?area={pivot_code}&type={contr_type}&out=xls"
            download_url_and_dataframe_update(url=url_temp, filter_category=cat, contribution_name=contr_type)