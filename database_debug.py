import dataset
import psycopg2
import pandas as pd
import sys

db = dataset.connect('postgresql://Nickwang3:urfhjtyy1!@postgresql-test-baseball.cs3khvsyqwtx.us-east-2.rds.amazonaws.com:5432/baseballstats_test')

table1 = db['players']
table2 = db['batting_stats']

result1 = db.query("SELECT * FROM players where mlb_name = 'Alex Katz' ")
result2 = db.query("SELECT * FROM players where team = 'BOS' ")
result = db.query("SELECT * FROM batting_stats where espn_name = 'Adam Jones'")

for row in result2:
	print(row['espn_name'], row['position'], row['current_salary'])

for row in result:
	print(row['AVG'], row['HR'])
