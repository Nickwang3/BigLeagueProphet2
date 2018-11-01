import bs4
import re
from urllib.request import urlopen as uReq
from urllib.request import urlretrieve
from bs4 import BeautifulSoup as soup
import csv
import requests
import pandas as pd

def main():

	url = 'http://crunchtimebaseball.com/baseball_map.html'

	data = requests.get('http://crunchtimebaseball.com/master.csv').text

	with open('data/IDS.csv', 'w', encoding='utf8') as file:
   		file.write(data)


	my_url = "https://www.usatoday.com/sports/mlb/salaries/"

	#using pandas to read the career statistics
	salary_data = pd.read_html(requests.get(my_url).text)

	salary_data = salary_data[0]

	#renaming some columns for easier data grabbing
	salary_data.rename(columns={'Total Value':'Total_Value'}, inplace=True)
	salary_data.rename(columns={'Avg Annual':'Avg_Annual'}, inplace=True)

	#extract length of contract
	def label_length (row):
		years = row['Years']
		length = int(years[:years.index("(")].strip())
		return length

	#extract years contract is active
	def label_years (row):
		years = row['Years']
		indx_paren = years.index("(")
		indx_close = years.index(")")
		years = str(years[indx_paren+1:indx_close].strip())
		return years

	#extract year contract is signed
	def label_year_signed (row):

		years = row['Years']
		indx_paren = years.index("(")
		indx_dash = years.find("-")
		year_signed = int(years[indx_paren+1:indx_dash])
		return year_signed

	def label_int_value (row):
		salary = row['Total_Value']
		salary = int(salary[1:].replace(",", ""))
		return salary

	def label_int_annual (row):
		salary = row['Avg_Annual']
		salary = int(salary[1:].replace(",", ""))
		return salary

	def label_int_salary (row):
		salary = row['Salary']
		salary = int(salary[1:].replace(",", ""))
		return salary

	salary_data['Contract_Length'] = salary_data.apply (lambda row: label_length (row),axis=1)
	salary_data['Years_Active'] = salary_data.apply (lambda row: label_years (row),axis=1)
	salary_data['Years_Signed'] = salary_data.apply (lambda row: label_year_signed (row),axis=1)
	salary_data['int_value'] = salary_data.apply (lambda row: label_int_value (row),axis=1)
	salary_data['int_annual'] = salary_data.apply (lambda row: label_int_annual (row),axis=1)
	salary_data['int_salary'] = salary_data.apply (lambda row: label_int_salary (row),axis=1)


	#writing the csv file
	salary_data.to_csv("data/salary_data.csv", index=False)


main()
