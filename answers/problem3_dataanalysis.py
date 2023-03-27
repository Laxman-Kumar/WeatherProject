import pandas as pd
from ConnectionClass import PostgreConnection
import psycopg2.extras as extras


pg_obj = PostgreConnection('localhost','postgres',"postgres","0208")

conn = pg_obj.connect()
curr = conn.cursor()


curr.execute("Select * from weather_data")
weather_data = curr.fetchall()

df = pd.DataFrame(weather_data, columns=['sn','station','date','max_temp','min_temp','precipitation'])
df['year'] = df['date'].apply(lambda x: x[:4])

#columns : id, station_id, year, avg_max_temp, avg_min_temp, total_precipitation
result = []

for row in df.groupby(['station','year']):
    data = row[1]
    max_temp = (data[data['max_temp']!=-9999.0]['max_temp'].mean())/10
    min_temp = (data[data['min_temp']!=-9999.0]['min_temp'].mean())/10
    total_prec = (data[data['precipitation']!=-9999.0]['precipitation'].sum()) /100
    result.append([row[0][0], row[0][1], max_temp, min_temp, total_prec])


df2 = pd.DataFrame(result, columns=['station_id', 'year', 'avg_max_temp', 'avg_min_temp', 'total_precipitation'])

#create table

curr.execute('''
                CREATE TABLE IF NOT EXISTS weather_stats (
                id SERIAL PRIMARY KEY,
                station_id VARCHAR(12),
                year INTEGER,
                avg_max_temp REAL,
                avg_min_temp REAL,
                total_precipitation REAL
                );
             ''')
conn.commit()

tuples = [tuple(x) for x in df2.to_numpy()]

query = "INSERT INTO weather_stats(station_id, year, avg_max_temp, avg_min_temp, total_precipitation) values %s"

extras.execute_values(curr, query, tuples)

conn.commit()

conn.close()