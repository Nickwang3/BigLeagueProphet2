#library for database retrieval methods
from sqlalchemy import create_engine
import pandas as pd
import numpy as np

def get_stats_as_df(mlb_id, engine):

    query1 = 'SELECT * FROM players WHERE "MLB_ID" = %(id)s'
    player_info = pd.read_sql(query1, con=engine, params={'id':mlb_id})

    for row in player_info.itertuples(index=True, name='Pandas'):
        espn_id = getattr(row, "ESPN_ID")
        position = getattr(row, "POSITION")

    if position == 'P':
        query2 = ('SELECT * FROM pitchingstats WHERE "ESPN_ID" = %(id)s')
        stats = pd.read_sql(query2, con=engine, params={'id':espn_id})
    else:
        query2 = ('SELECT * FROM battingstats WHERE "ESPN_ID" = %(id)s')
        stats = pd.read_sql(query2, con=engine, params={'id':espn_id})

    return stats

def get_list_of_ids(engine):

    query1 = 'SELECT "MLB_ID" FROM players'
    mlb_id_list = pd.read_sql(query1, con=engine)

    mlb_id_list = mlb_id_list.values.flatten()
    return mlb_id_list

def get_player_info_as_dict(mlb_id, engine):

    query1 = 'SELECT * FROM players WHERE "MLB_ID" = %(id)s'
    player_info = pd.read_sql(query1, con=engine, params={'id':mlb_id})

    player_info = player_info.to_dict(orient='list')
    for key in player_info:
        player_info[key] = player_info[key][0]

    return player_info
