from answers.ConnectionClass import PostgreConnection
import os
import time
import pandas as pd

pg_obj = PostgreConnection('localhost','postgres','postgres','0208')

conn = pg_obj.connect()
curr = conn.cursor()

start = time.time()
total_record = 0

#fetching all the record from database

curr.execute("SELECT * FROM weather_data")
weather_data = curr.fetchall()

weather_data_df = pd.DataFrame(weather_data, columns=['SN','station','date','max_temp','min_temp','precipitation'])

# Loop through each weather station file
for filename in os.listdir('wx_data'):
    # Open the file for reading
    with open(os.path.join('wx_data', filename), 'r') as file:
        # Loop through each line in the file
        station = filename.split(".")[0]
        for line in file:
            
            # Split the line into its fields
            date, max_temp, min_temp, precip = line.strip().split('\t')
            if len(weather_data_df.loc[(weather_data_df['station']==station) & (weather_data_df['date']==date)])==0:
                total_record+=1
                    # Insert the data into the database
                curr.execute('INSERT INTO weather_data (station_id, date, max_temp, min_temp, precipitation) VALUES (%s, %s, %s, %s, %s)', (station, date, max_temp, min_temp, precip))

   
        conn.commit()
        
conn.close()
end=time.time()

print("Total number of records inserted are {}".format(total_record))
print("Total time: {}".format(end-start))
    
