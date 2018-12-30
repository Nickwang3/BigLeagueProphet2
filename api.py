#library for backend restful api
from flask import Flask
from flask_restful import Api, Resource, reqparse
from sqlalchemy import create_engine
from json import dumps
from flask import jsonify


engine = create_engine('postgresql://awsnick:nickadmin@playersdatabase.cs3khvsyqwtx.us-east-2.rds.amazonaws.com:5432/players', echo=False)
app = Flask(__name__)
api = Api(app)


class Players(Resource):

    __tablename__ = 'players'

    def get(self):
        conn = engine.connect()
        query = conn.execute('select * from players')
        result = {'player objects': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
        return jsonify(result)

# class Search(Resource):
#
#     __tablename__ = 'players'
#
#     def get(self):
#         conn = engine.connect()
#         query = conn.execute('select ')


api.add_resource(Players, '/players')   #first route

if __name__ == '__main__':
     app.run(port='5002')
