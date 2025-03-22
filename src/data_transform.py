import polars as pl
import json
import os

with open('data/movie.json', 'r') as f:
    data = json.load(f)

"""
The data is in the following format:

"""
## I want to format the data so that each title is a separate entry in the DataFrame
movies_df = pl.DataFrame(data['movies'])
pc_df = pl.DataFrame(data['production_companies'])
genre_df = pl.DataFrame(data['genres'])

## Merging the 3 dataframes based on the movie_id
formatted_data = movies_df.join(pc_df, on='id', how='left').join(genre_df, on='id', how='left')
# print(formatted_data.head())
# df = formatted_data
# print(df.head())
# null_counts = df.null_count()
# print(null_counts)
def transfrom_data(df=formatted_data):
    df = pl.DataFrame(formatted_data)
    try:
        try:
            # replacing null values with 0 in integer columns
            df = df.with_columns(
                pl.col("start_year").fill_null(0),
                pl.col("end_year").fill_null(0),
                pl.col("runtime_minutes").fill_null(0),
                pl.col("num_votes").fill_null(0),
                pl.col("average_rating").fill_null(0)
            )
        except Exception as e:
            print(f"Error replacing null values with 0 in integer columns: {e}")
        
        try:
            # replacing null values with 0 in float columns and remove null rows in releaseDate and ensure only unique rows in id column
            df = df.filter(pl.col("release_date").is_not_null())
            df = df.filter(
                pl.col("genre").is_not_null())
            df = df.unique(subset=["id"])
            df = df.unique(subset=["copmany_id"])
        except Exception as e:
            print(f"Error replacing null values with 0 in float columns: {e}")
        
        try:
            # conversion of string columns to datetime
            df = df.with_columns(
                pl.col('release_date').str.to_date('%Y-%m-%d')
            )
        except Exception as e:
            print(f"Error converting string columns to datetime: {e}")
        
        try:
            # conversion of string columns to integer
            df = df.with_columns(
                pl.col('start_year').cast(pl.Int32),
                pl.col('end_year').cast(pl.Int32),
                pl.col('runtime_minutes').cast(pl.Int32),
                pl.col('num_votes').cast(pl.Int32),
                pl.col('average_rating').cast(pl.Float32)
            )
        except Exception as e:
            print(f"Error converting string columns to integer: {e}")        
        return df
    except Exception as e:
        print(f"Error transforming data: {e}")
        return None


if __name__ == '__main__':
    trans_data = transfrom_data(df = pl.DataFrame(formatted_data))
    # print(trans_data.head())
    folder_path = 'data/'
    csv_path = os.path.join(folder_path, 'movies.csv')
    trans_data.write_csv(csv_path)
    print(f'Movie csv file saved to {csv_path}')
    parquet_path = os.path.join(folder_path, 'movies.parquet')
    trans_data.write_parquet(parquet_path)
    print(f'Movie parquet file saved to {parquet_path}')
#     # trans_data.write_csv('data/movies.csv')
#     # trans_data.write_parquet('data/movies.parquet')
#     # print(trans_data.null_count())
#     # print(trans_data.columns)