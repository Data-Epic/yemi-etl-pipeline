import logging

from src.db_loader import Database
from src.web_scraper import fetch_data, flatten_data, store_moveis_data
from src.data_transform import transfrom_data
from src.db_loader import Database


def main():
    logging.basicConfig(
        # filename='logs.log',
        level=logging.INFO,
        format="%(asctime)s - %(message)s",
        datefmt="%d-%b-%y %H:%M:%S",
    )
    logging.info("Starting the ETL process")
    try:
        # Fetch data from rapid api and extract important information
        logging.info("Web-scraper is running......")
        logging.info("Fetching data from RapidAPI......")
        data = fetch_data()
        logging.info(f"Scraped/Fetched {len(data)} records")
        logging.info("Flattening the data.........")
        flattened_data = flatten_data(data)
        logging.info("Storing the data")
        store_moveis_data()
        logging.info("Data stored successfully")

        # Transform the data with polars, remove null values, and convert data types, and drop duplicates for ids
        logging.info("data-transformer is runninng......")
        logging.info("Transforming the data.....")
        transformed_data = transfrom_data()
        logging.info("Data transformed successfully")
        logging.info(f"Shape of Transformed data: {transformed_data.shape}")
        logging.info(f"Transformed data: {transformed_data}")

        # Load the data into movies database
        logging.info("db-loader is running......")
        logging.info("Loading the data into the database.......")
        db = Database()
        db.add_data()
        logging.info("Data loaded successfully")
        db.close()
        logging.info("Database connection closed")
    except Exception as e:
        logging.error(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
    logging.info("ETL process completed successfully")
