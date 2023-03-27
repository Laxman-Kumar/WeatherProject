-- DATABASE USED POSTGRES

CREATE TABLE weather_data (
    id SERIAL PRIMARY KEY,
    station_id VARCHAR(12) NOT NULL,
    date TEXT NOT NULL,
    max_temp FLOAT,
    min_temp FLOAT,
    precipitation FLOAT
);

CREATE TABLE crop_yield_data(
	id SERIAL PRIMARY KEY,
	year INTEGER NOT NULL,
	yield INTEGER NOT NULL
);