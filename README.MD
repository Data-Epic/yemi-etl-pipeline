# ETL Pipeline with RapidAPI
## Project overview
This project is an end-to-end ETL pipeline that scrapes/fetches movie data, transforms it with polars and laods it into a postgres database.

## Features
1. Extracts IMDb movie data from RapidAPI and reformats the data to extract required information and writes it into a json file
2. Dta cleaning and transformation: Processes raw data in the json file using polars.
3. Loads the cleaned data into postgres database using SQLAlchemy.
4. ETL pipeline: Combines steps 1 to 3 in a structured pipeline and uses `Logging` to monitor the execution of each step in the pipeline.

## Database schema and ERD diagram
![Schema image](schema.png)
![ERD Diagram](erd.png)
