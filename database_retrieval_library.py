#library for database retrieval methods
from sqlalchemy import create_engine
import pandas as pd

def get_stats_as_df(mlb_id):

    engine = create_engine('postgresql://awsnick:nickadmin@playersdatabase.cs3khvsyqwtx.us-east-2.rds.amazonaws.com:5432/players', echo=False)
    query1 = 'SELECT * FROM players WHERE mlb_id = id:'
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
