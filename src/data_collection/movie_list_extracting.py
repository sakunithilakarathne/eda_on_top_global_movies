
import requests
from bs4 import BeautifulSoup
import pandas as pd


def get_imdb_movies(sort_parameter):
    """
    Scrape IMDB website according to the specified parameter
    """

    # URL for scraping IMDB
    base_url = "https://www.imdb.com/search/title/"
    # Genre list available in IMDB
    genre_list = ["action", "adventure", "animation", "biography", "comedy", "crime", "family", "fantasy", "history",
                  "horror", "music", "musical", "mystery", "romance", "sport", "thriller", "war", "western"]

    # List to store all movie titles and IMDB IDs
    all_movie_data = []

    for each_genre in genre_list:
        params = {
            "genres": each_genre,
            "explore": "genres",
            "title_type": "feature",
            "num_votes": "100000,",
            "sort": sort_parameter
        }

        # Set headers to avoid blocking
        headers = {"User-Agent": "Mozilla/5.0"}

        # Fetch the page content
        imdb_response = requests.get(base_url, params=params, headers=headers)
        soup = BeautifulSoup(imdb_response.text, "html.parser")

        # Find all movie titles using the class id
        movie_details = soup.find_all('div', class_="sc-d5ea4b9d-0 ejavrk")

        # Extract and store movie titles
        for movie in movie_details:
            movie_title = movie.find('h3', class_="ipc-title__text").text.split(".")[1]
            movie_id = movie.find('a', class_='ipc-title-link-wrapper').get('href').split('/')[2]

            all_movie_data.append({
                "Title": movie_title,
                "IMDb ID": movie_id
            })

    # Creating a dataframe for the extracted data
    df = pd.DataFrame(data=all_movie_data)

    # Removing duplicate values in the data frame
    df_cleaned = df.drop_duplicates(subset=["IMDb ID"]).reset_index(drop=True)

    return df_cleaned