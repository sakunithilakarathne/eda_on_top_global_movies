import pandas as pd

from src.data_collection.movie_list_collection import *
from src.data_collection.individual_movie_data_collection import *

def main():
    try:
        year = 2007
        movie_list_df = pd.read_csv(f"data/raw_data/movies_of_{year}.csv")
        new_data_df = asyncio.run(extract_individual_movies(movie_list_df))
        df_updated = movie_list_df.merge(new_data_df, on='imdb_id', how='left')
        df_updated.to_csv(f"data/raw_data/datasets_of_each_year/dataset_of_{year}.csv",index = False)


        dataframes = []
        #for year in range(2000,2002):
        #     movie_list_df = asyncio.run(extract_movie_lists(year=year))
        #     new_data_df = asyncio.run(extract_individual_movies(movie_list_df))
        #     # Merge the new data with the existing DataFrame based on 'imdb_id'
        #     df_updated = movie_list_df.merge(new_data_df, on='imdb_id', how='left')
        #     df_updated.to_csv(f"data/raw_data/datasets_of_each_year/movies_of_{year}.csv",index = False)
        #     dataframes.append(df_updated)
        #
        # combined_dataset = pd.concat(dataframes,ignore_index=True)
        # combined_dataset.to_csv("data/raw_data/imdb_movie_data.csv",index = False)

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        print("Completed !")








if __name__ == "__main__":
    main()