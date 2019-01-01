#manipulation of stats for players
import pandas as pd
import sys
# from sqlalchemy import create_engine
# engine = create_engine('postgresql://awsnick:nickadmin@playersdatabase.cs3khvsyqwtx.us-east-2.rds.amazonaws.com:5432/players', echo=False)


#gets rid of rows where of same year only keeps total stats
def only_total_rows(position, stats):

	if position == 'SP' or position == 'RP':
		key = "SEASON"
	else:
		key = "YEAR"

	year = ''
	list_of_unwanted_indices = []

	for i in range(len(stats.index)):

		if stats['TEAM'][i] == 'Total':

			year = stats[key][i]

			for k in range(len(stats.index)):

				if stats[key][k] == year and stats['TEAM'][k] != 'Total':

					list_of_unwanted_indices.append(k)

	stats = stats.drop(stats.index[list_of_unwanted_indices])
	stats = stats.reset_index()

	return stats


#gets the career average for a stat
def average_stat(player_stats, statistic):

	total = 0
	# for i in range(len(player_stats.index)):
	# 	total = total + player_stats[statistic][i]
	total = player_stats[statistic].sum()

	if len(player_stats.index) == 0:
		return

	try:
		average = total / (len(player_stats.index))
	except:
		return

	average = float("{0:.2f}".format(average))

	return average


def career_high_stat(player_stats, statistic):

	career_high = 0

	# for i in range(len(player_stats.index)):
	# 	if player_stats[statistic][i] > career_high:
	# 		career_high = player_stats[statistic][i]

	try:
		career_high = player_stats[statistic].max()
	except:
		career_high = None

	# if career_high == -10:
	# 	return None

	return career_high


def weight_last_3(player_stats, statistic, last_completed_year):

	stats = player_stats
	last_full_mlb_season = last_completed_year
	first_year = last_full_mlb_season - 2

	first = 0
	second = 0
	third = 0
	for i in range(len(stats.index)):
		try:
			if int(stats['SEASON'][i]) == first_year:
				first = float(stats[statistic][i]) * .75
			if int(stats['SEASON'][i]) == first_year + 1:
				second = float(stats[statistic][i])
			if int(stats['SEASON'][i]) == last_full_mlb_season:
				third = float(stats[statistic][i]) * 1.25

		except KeyError:
			if int(stats['YEAR'][i]) == first_year:
				first = float(stats[statistic][i]) * .75
			if int(stats['YEAR'][i]) == first_year + 1:
				second = float(stats[statistic][i])
			if int(stats['YEAR'][i]) == last_full_mlb_season:
				third = float(stats[statistic][i]) * 1.25

	try:
		weighted_total = first + second + third
		weighted_total = float("{0:.2f}".format(weighted_total))
	except:
		weighted_total = None

	return weighted_total


# espn_id = '6341'
# query2 = ('SELECT * FROM pitchingstats WHERE "ESPN_ID" = %(id)s')
# stats = pd.read_sql(query2, con=engine, params={'id':espn_id})
# war = weight_last_3(stats, 'WAR', 2017)
# print(war)
