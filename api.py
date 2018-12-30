#library for backend restful api
from flask import Flask
from flask_restful import Api, Resource, reqparse
from sqlalchemy import create_engine, text
from json import dumps
from flask import jsonify




engine = create_engine('postgresql://awsnick:nickadmin@playersdatabase.cs3khvsyqwtx.us-east-2.rds.amazonaws.com:5432/players', echo=False)
app = Flask(__name__)
api = Api(app)

#access all player information
class Players(Resource):

    __tablename__ = 'players'

    def get(self):
        conn = engine.connect()
        query = conn.execute('SELECT * FROM players')
        result = {'player objects': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
        return jsonify(result)

#access a specific player's information based on mlb_id
class Search_by_mlb_id(Resource):

    __tablename__ = 'players'

    def get(self, mlb_id):
        conn = engine.connect()
        statement = text('SELECT * FROM players WHERE "MLB_ID" = :id')
        query = conn.execute(statement, id=mlb_id)
        result =  {'player': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
        return jsonify(result)

#returns stats for player in json format (stat columns are in alpahbetical order, needs to be reformatted)
class Stats(Resource):

    # should change to not even needing ESPN_ID (needs conversion from mlb to espn)
    def get(self, mlb_id):
        conn = engine.connect()
        grab_id = text('SELECT "ESPN_ID" FROM players WHERE "MLB_ID" = :id')
        query_id = conn.execute(grab_id, id=mlb_id)
        # espn_id = query_id.cursor
        for i in query_id.cursor:
            id_list = i
        espn_id = id_list[0]

        #check position for correct stats
        grab_position = text('SELECT "POSITION" FROM players WHERE "MLB_ID" = :id')
        query_position = conn.execute(grab_position, id=mlb_id)

        for i in query_position.cursor:
            position_list = i
        position = position_list[0]

        if position == 'P':
            statement = text('SELECT * FROM pitchingstats WHERE "ESPN_ID" = :id')
            query = conn.execute(statement, id=espn_id)
            result =  {'pitching stats': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
        else:
            statement = text('SELECT * FROM battingstats WHERE "ESPN_ID" = :id')
            query = conn.execute(statement, id=espn_id)
            result =  {'batting stats': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}

        return jsonify(result)


api.add_resource(Players, '/players')   #first route
api.add_resource(Search_by_mlb_id, '/search/id/<mlb_id>') #second route
api.add_resource(Stats, '/stats/id/<mlb_id>')  #third route


if __name__ == '__main__':
     app.run(port='5002', debug=True)
