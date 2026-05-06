import re
import csv

input_file="WhatsAppChatwithAIKeralamCommunity-6may26_9.25am.txt"
output_file="linkedin_profiles.csv"

pattern = r"https?://(?:www\.)?linkedin\.com/in/[A-Za-z0-9\-_%]+/?"

with open(input_file,"r", encoding="utf-8") as f:
    text=f.read()

links=sorted(set(re.findall(pattern, text)))

with open(output_file,"w",newline="",encoding="utf-8") as f:
    writer=csv.writer(f)
    writer.writerow(["linkedin_url","status","note"])
    for link in links:
        writer.writerow([link,"pending",""])

print(f"Found {len(links)} Linkedin profiles")