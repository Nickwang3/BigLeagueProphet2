import bs4
import re
from urllib.request import urlopen as uReq
from urllib.request import urlretrieve
from bs4 import BeautifulSoup as soup
import csv
import requests
import pandas as pd
from sqlalchemy import create_engine
from data.globalvar import current_year, last_completed_season

engine = create_engine('postgresql://awsnick:nickadmin@playersdatabase.cs3khvsyqwtx.us-east-2.rds.amazonaws.com:5432/players', echo=False)


#parse through the espn free agent tracker signings, grab link to
#player's espn id and contract value and years
#espn id will be used to gather player stats and train data

#free agent signings from 2010 till most recent offseason are to be tracked
yeariter = 2010
# mostrecentseason = 2018
# currentyear = 2018
print(current_year)
print(last_completed_season)

free_agent_signings = pd.DataFrame(columns=['ESPN_ID', 'ESPN_NAME', 'AGE', 'POSITION', 'YEARS', 'TOTAL_VALUE'])


while yeariter < last_completed_season:

# my_url = "http://www.espn.com/mlb/freeagents"
    my_url = "http://www.espn.com/mlb/freeagents/_/year/" + str(yeariter)

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
        current_age = tds[2].text
        try:
            age_at_signing = str(int(current_age) - (current_year - yeariter))
        except ValueError:
            pass

        years = tds[6].text
        total_value = tds[8].text

        total_value = total_value[1:]
        total_value = total_value.replace(',', '')

        for td in tds:
            print (td.text, end=" ")
        print()

        df = pd.DataFrame([[espn_id, espn_name, age_at_signing, position, years, total_value]], columns=['ESPN_ID', 'ESPN_NAME', 'AGE', 'POSITION', 'YEARS', 'TOTAL_VALUE'])
        free_agent_signings = free_agent_signings.append(df)


    yeariter += 1

#formatting the data
free_agent_signings = free_agent_signings[(free_agent_signings['TOTAL_VALUE']!='inor Lg') & (free_agent_signings['TOTAL_VALUE']!='-') & (free_agent_signings['TOTAL_VALUE']!='OLLARS')]

#store the data
free_agent_signings.to_sql('freeagentsignings', con=engine, chunksize=1000, if_exists='replace')
free_agent_signings.to_csv('data/free_agent_signings.csv')
