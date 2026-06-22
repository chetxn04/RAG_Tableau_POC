import zipfile 
import os

def explore_workbook(twbx_path, extract_to):
    with zipfile.ZipFile(twbx_path, 'r') as z:
        names = z.namelist()
        z.extractall(extract_to)
    print(f"\n--- Contents of {twbx_path} ---")

    for n in names: 
        print(n)

    return names

superstore_files = explore_workbook("superstore.twbx", "extracted_superstore")
covid_files = explore_workbook("covid.twbx", "extracted_covid")


