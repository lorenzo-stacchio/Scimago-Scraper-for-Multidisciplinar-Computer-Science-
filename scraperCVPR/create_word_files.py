from docx import Document
import os, shutil
import pandas as pd
import re

def clean_filename(filename, replacement='_', max_length=255):
    # Remove invalid characters
    filename = re.sub(r'[<>:"/\\|?*]', replacement, filename)
    
    # Trim leading and trailing whitespace
    filename = filename.strip()
    
    # Limit the length of the filename
    if len(filename) > max_length:
        filename = filename[:max_length]
        
    return filename

if __name__ == "__main__":
    out_dir = "scraperCVPR/word_files/"

    if os.path.exists(out_dir):
        shutil.rmtree(out_dir)
    os.mkdir(out_dir)

    df = pd.read_excel("scraperCVPR/data_with_urls_FINAL.xlsx")
    
    for i,paper in enumerate(df["paper"]):
        # Create a new Document
        doc = Document()
        paper_name = clean_filename(paper)
        # Save the document with a specific name
        doc.save(f'{out_dir}{i+1}_{paper_name}.docx')




