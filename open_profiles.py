import csv
import webbrowser
import time

with open("linkedin_profiles.csv", "r",encoding="utf-8") as f:
    reader=csv.DictReader(f)
    for row in reader:
        if row["status"]=="pending":
            webbrowser.open(row["linkedin_url"])
            time.sleep(8)