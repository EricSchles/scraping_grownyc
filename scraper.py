import requests
import lxml.html
import pandas as pd
from unidecode import unidecode

header = ["BOROUGH","GREENMARKET","DAY","TIME","PARTNER"]
df = pd.DataFrame()
r = requests.get("http://www.grownyc.org/compost/locations")
html = lxml.html.fromstring(r.text)
rows = ["tmp"] + html.xpath("//tbody/tr//td") #this is all the values of the table
table = []
tmp = []
for ind,row in enumerate(rows):
    if row != "tmp": 
        tmp.append(unidecode(row.text_content().replace("\n","").replace("\t","")))
    else:
        tmp.append(row)
    if ind != 0 and ind % 5 == 0:
        table.append(tmp)
        tmp = []

table[0].remove("tmp")

for row in table:
    tmp_dict = {}
    for ind,value in enumerate(header):
        tmp_dict[value] = row[ind]
    df = df.append(tmp_dict,ignore_index=True)

df.to_csv("food_waste.csv")
