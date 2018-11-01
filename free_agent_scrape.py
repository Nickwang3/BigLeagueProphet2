import bs4
import re
from urllib.request import urlopen as uReq
from urllib.request import urlretrieve
from bs4 import BeautifulSoup as soup
import csv
import requests
import pandas as pd



#parse through the espn free agent tracker signings, grab link to
#player's espn id and contract value and years
#espn id will be used to gather player stats and train data



my_url = "http://www.espn.com/mlb/freeagents"

page_html = requests.get(my_url).text
page_soup = soup(page_html, "html.parser")

table = page_soup.find('table')

rows = table.find_all("tr")
rows = rows[2:]

#looking at each row in freeagents table
for row in rows:
    href = row.find('a', href=True)


    #grab espn_id from href
    try:
        link = href.get('href')
        print(link)
        link = link[36:]
        link = link.replace("/", " ")
        lst = link.split()
        espn_id = lst[0]
        print(espn_id)
    except (AttributeError):
        pass


    #parse through data of each row
    tds = row.find_all("td")

    espn_name = tds[0].text
    position = tds[1].text
    age_at_signing = tds[2].text
    years = tds[6].text
    total_value = tds[8].text

    for td in tds:
        print (td.text, end=" ")
    print()


    print(espn_name, espn_id, total_value, years)
