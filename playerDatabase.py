# Here we will add all players that are currently active or were active recently
#import psycopg2
import pandas as pd
import sys
from scrape_stats import getPlayerStats
from sqlalchemy import create_engine




errorlog = pd.DataFrame(columns=['ESPN_ID', 'ESPN_NAME', 'MLB_NAME'])

count = 0
#connect to postgres database on aws using dataset library and sqlalchemy
engine = create_engine('postgresql://awsnick:nickadmin@playersdatabase.cs3khvsyqwtx.us-east-2.rds.amazonaws.com:5432/mlb', echo=False)

#update ids and salary data

#creating player_id and salary_data dataframe in pandas
player_IDS = pd.read_csv('data/IDS.csv', encoding='ANSI')
salary_data = pd.read_csv('data/salary_data.csv')

#datatables and their columns
playerscol = ['MLB_ID', 'MLB_NAME', 'ESPN_NAME', 'CBS_NAME', 'ESPN_ID', 'TEAM', 'POSITION', 'BIRTH_YEAR', 'BATS', 'THROWS', 'SIGN_YEAR', 'YEARS_ACTIVE', 'LENGTH', 'TOTAL_VALUE', 'AVG_VALUE', 'CURRENT_SALARY']
players = pd.DataFrame(columns=playerscol)

battingcols = ['YEAR','TEAM','GP', 'AB', 'R', 'H', '2B', '3B', 'HR', 'RBI', 'BB', 'SO', 'SB', 'CS', 'AVG', 'OBP', 'SLG', 'OPS', 'WAR', 'ESPN_ID']
battingstats = pd.DataFrame(columns=battingcols)

pitchingcols = ['SEASON', 'TEAM', 'GP', 'GS', 'CG', 'SHO', 'IP', 'H', 'R', 'ER', 'HR', 'BB', 'SO', 'W', 'L', 'SV', 'HLD', 'BLSV', 'WAR', 'WHIP', 'ERA', 'ESPN_ID']
pitchingstats = pd.DataFrame(columns=pitchingcols)

#iterating through dataframe and placing data into database
rows1 = []
for row in player_IDS.itertuples(index=True, name='Pandas'):


    mlb_id = str(getattr(row, "mlb_id"))

    try:
        mlb_name = str(getattr(row, "mlb_name"))
    except ValueError:
        mlb_name = 'null'
    try:
        espn_name = str(getattr(row, "espn_name"))
    except ValueError:
        espn_name = 'null'
    try:
        cbs_name = str(getattr(row, "cbs_name"))
    except ValueError:
        cbs_name = 'null'
    try:
        position = str(getattr(row, "mlb_pos"))
    except ValueError:
        position = 'null'
    try:
        team = str(getattr(row, "mlb_team"))
    except ValueError:
        team = 'null'
    try:
        espn_id = str(int(getattr(row, "espn_id")))
    except ValueError:
        espn_id = 'null'
    try:
        birth_year = int(getattr(row, "birth_year"))
    except ValueError:
        birth_year = 'null'
    try:
        bats = str(getattr(row, "bats"))
    except ValueError:
        bats = 'null'
    try:
        throws = str(getattr(row, "throws"))
    except ValueError:
        throws = 'null'


    #handle if one of the names is missing copy it over to the other
    if espn_name == 'nan':
        if cbs_name != 'nan':
            espn_name = cbs_name
        elif mlb_name != 'nan':
            espn_name = mlb_name
    if mlb_name == 'nan':
        if cbs_name != 'nan':
            mlb = cbs_name
        elif espn_name != 'nan':
            mlb_name = espn_name
    if cbs_name == 'nan':
        if espn_name != 'nan':
            cbs_name = espn_name
        elif mlb_name != 'nan':
            cbs_name = mlb_name


    contract_df = []
	#check if player is in salary data base (could be under a few possible names)
    if mlb_name in salary_data.Name.values:
        contract_df = salary_data[salary_data.Name==mlb_name]
    elif espn_name in salary_data.Name.values:
        contract_df = salary_data[salary_data.Name==espn_name]
    elif cbs_name in salary_data.Name.values:
        contract_df = salary_data[salary_data.Name==cbs_name]
    else:
        contract_df = None #no contract is found for player

	#checking if there are players with the same name
    try:
        if len(contract_df.index) > 1:
            for row in contract_df.itertuples(index=True, name='Pandas'):
                if contract_df[contract_df.POS!=position]:
                    contract_df.drop(row)
                elif contract_df[contract_df.Team!=team]:
                    contract_df.drop(row)
    except:
        print(espn_name, "no contract")


    #get contract data
    try:
        for row in contract_df.itertuples(index=True, name='Pandas'):
            sign_year = int(getattr(row, "Years_Signed"))
            years_active = getattr(row, "Years_Active")
            length = int(getattr(row, "Contract_Length"))
            total_value = int(getattr(row, "int_value"))
            avg_value = int(getattr(row, "int_annual"))
            current_salary = int(getattr(row, "int_salary"))

    except AttributeError:
        sign_year = 'null'
        years_active = 'null'
        length = 'null'
        total_value = 'null'
        avg_value = 'null'
        current_salary = 'null'


    #grabbing player stats
    try:
        stats = getPlayerStats(espn_id, espn_name)
        stats['ESPN_ID'] = espn_id
        print(stats)
    except:
        print(espn_name)
        print(espn_id)
        continue

    #concat the dataframes with the new players data
    playerrow = pd.DataFrame([mlb_id, mlb_name, espn_name, cbs_name, espn_id, team, position, birth_year, bats, throws, sign_year, years_active, length, total_value, avg_value, current_salary], columns=playerscol)
    players = pd.concat([players, playerrow])

    if list(stats.columns.values) == battingcols:
        battingstats = pd.concat([battingstats, stats])
    elif list(stats.columns.values) == pitchingcols:
        pitchingstats = pd.concat([pitchingstats, stats])
    else:
        playererror = pd.DataFrame([[espn_id, espn_name, mlb_name]], columns=['ESPN_ID', 'ESPN_NAME', 'MLB_NAME'])
        errorlog = pd.concat([errorlog, playererror])


    print(count)
    count+=1



#storing into the database and a backup csv file
battingstats.to_sql('battingstats', con=engine, chunksize=1000, if_exists='replace')
pitchingstats.to_sql('pitchingstats', con=engine, chunksize=1000, if_exists='replace')
players.to_sql('players', con=engine, chunksize=1000, if_exists='replace')

errorlog.to_csv('data/errorlog.csv')
battingstats.to_csv('data/battingstats.csv')
pitchingstats.to_csv('data/pitchingstats.csv')
players.to_csv('data/pitchingstats.csv')
