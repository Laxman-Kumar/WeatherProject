from flask_restful import Api, Resource, fields, reqparse

from flask import Flask, request
from ConnectionClass import PostgreConnection

from flask_restful_swagger import swagger

from flask_apispec import marshal_with, doc, use_kwargs
from flask_apispec.views import MethodResource
from marshmallow import Schema, fields

from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from flask_apispec.extension import FlaskApiSpec

#from werkzeug.utils import cached_property 
#werkzeug.cached_property = werkzeug.utils.cached_property


app = Flask(__name__)
#api = Api(app)
api = swagger.docs(Api(app), apiVersion='0.1')

app.config.update({
    'APISPEC_SPEC': APISpec(
        title='Weather Project',
        version='v1',
        plugins=[MarshmallowPlugin()],
        openapi_version='2.0.0'
    ),
    'APISPEC_SWAGGER_URL': '/weather_project/',  # URI to access API Doc JSON 
    'APISPEC_SWAGGER_UI_URL': '/swagger-ui/'  # URI to access UI of API Doc
})


docs = FlaskApiSpec(app)


pg_obj = PostgreConnection('localhost','postgres',"postgres","0208")
conn = pg_obj.connect()

weather_response_schema = dict(
    station_id=fields.String(),
    date=fields.String(),
    max_temp=fields.String(),
    min_temp=fields.String(),
    precipation=fields.String()
) #  Restful way of creating APIs through Flask Restful


class WeatherSchema(Schema):
    station_id = fields.Str()
    date= fields.Str()
    max_temp=fields.Str()
    min_temp=fields.Str()
    precipitation=fields.Str()

class Weather(MethodResource,Resource):
    @use_kwargs({
            'station_id': fields.Str(),
            'from_date': fields.Str(),
            'to_date': fields.Str(),
            'page': fields.Str(),
            'per_page': fields.Str()
        }, location='query')
    @marshal_with(WeatherSchema(many=True))
    @doc(description='Get weather data', tags=['Weather'])
   
    def get(self, request=request, *args, **kwargs):
        # get query parameters for filtering and pagination
        params = request.args
        station_id = params.get('station_id')
        from_date = params.get('from_date')
        to_date = params.get('to_date')
        page = params.get('page', 1, type=int)
        per_page = params.get('per_page', 10, type=int)

        # build the SQL query based on the query parameters
        query = "SELECT * FROM weather_data where 1=1"
        if station_id:
            query += f" AND station_id='{station_id}'"
        if from_date:
            query += f" AND date>='{from_date}'"
        if to_date:
            query += f" AND date<='{to_date}'"
        query += f" ORDER BY date ASC OFFSET {(page-1)*per_page} LIMIT {per_page}"


        cursor = conn.cursor()
        cursor.execute(query)
        data= cursor.fetchall()
        print(data[:2])
        
        results = []
        for row in data:
            result = {
                'station_id': row[1],
                'date': row[2],
                'max_temp': row[3],
                'min_temp': row[4],
                'precipitation': row[5]
            }
            results.append(result)

        return results



weather_stats_response_schema = dict(
    station_id=fields.String(),
    year=fields.String(),
    avg_max_temp=fields.String(),
    avg_min_temp=fields.String(),
    total_precipation=fields.String()
) #  Restful way of creating APIs through Flask Restful

class WeatherStatsSchema(Schema):
    station_id = fields.Str()
    year= fields.Str()
    avg_max_temp=fields.Str()
    avg_min_temp=fields.Str()
    total_precipitation=fields.Str()

class WeatherStats(MethodResource, Resource):
    @use_kwargs({
            'station_id': fields.Str(),
            'year': fields.Integer(),
            'page': fields.Str(),
            'per_page': fields.Str()}, location='query')
    @marshal_with(WeatherStatsSchema(many=True))
    @doc(description='Get weather stat data', tags=['WeatherStat'])

    def get(self, request=request, *args, **kwargs):
        # get query parameters for filtering and pagination
        params = request.args
        station_id = params.get('station_id')
        year = params.get('year')
        page = params.get('page', 1, type=int)
        per_page = params.get('per_page', 10, type=int)

        # build the SQL query based on the query parameters
        query = "SELECT * FROM weather_stats where 1=1"
        if station_id:
            query += f" AND station_id='{station_id}'"
        if year:
            query += f" AND year='{year}'"
        query += f" ORDER BY year ASC OFFSET {(page-1)*per_page} LIMIT {per_page}"


        cursor = conn.cursor()
        cursor.execute(query)
        data= cursor.fetchall()
        print(data[:2])
        
        results = []
        for row in data:
            result = {
                'station_id': row[1],
                'year': row[2],
                'avg_max_temp': row[3],
                'avg_min_temp': row[4],
                'total_precipitation': row[5]
            }
            results.append(result)

        return results


api.add_resource(Weather, '/api/weather')
api.add_resource(WeatherStats, '/api/weather/stats')
docs.register(Weather)
docs.register(WeatherStats)


app.run(debug=True)