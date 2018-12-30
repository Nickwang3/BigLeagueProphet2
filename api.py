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

# class Stats(Resource):
#
#     __tablename__ = ''

api.add_resource(Players, '/players')   #first route
api.add_resource(Search_by_mlb_id, '/search/id/<mlb_id>') #second route

if __name__ == '__main__':
     app.run(port='5002', debug=True)
