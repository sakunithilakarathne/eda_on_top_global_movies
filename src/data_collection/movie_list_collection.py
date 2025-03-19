import aiohttp
import asyncio
from bs4 import BeautifulSoup
import pandas as pd
import json

# Function to fetch movie data asynchronously
async def fetch_movie_lists_data(session, base_url, params, headers, each_genre):
    try:
        async with session.get(base_url, params=params, headers=headers) as response:
            content = await response.text()
            soup = BeautifulSoup(content, 'html.parser')
            movieData = soup.find('script', id='__NEXT_DATA__')

            if movieData:
                json_data = json.loads(movieData.string)
                movies = json_data['props']['pageProps']['searchResults']['titleResults']['titleListItems']
                movie_list = []
                for movie in movies:
                    title_id = movie.get('titleId', 'N/A')
                    title_text = movie.get('titleText', 'N/A')
                    metascore = movie.get('metascore', 'N/A')
                    aggregate_rating = movie.get('ratingSummary', {}).get('aggregateRating', 'N/A')
                    vote_count = movie.get('ratingSummary', {}).get('voteCount', 'N/A')
                    release_year = movie.get('releaseYear', 'N/A')
                    release_date = movie.get('releaseDate') or {}
                    release_month = release_date.get('month', 'N/A')
                    runtime = movie.get('runtime', 'N/A')

                    movie_list.append({
                        "imdb_id": title_id,
                        "movie_title": title_text,
                        "genres": each_genre,
                        "imdb_rating": aggregate_rating,
                        "metascore": metascore,
                        "vote_count": vote_count,
                        "release_year": release_year,
                        "release_month": release_month,
                        "runtime": runtime
                    })
                return movie_list
            else:
                print(f"JSON data not found for genre: {each_genre}, params: {params}")
                return []
    except Exception as e:
        print(f"Error fetching data for genre {each_genre}: {e}")
        return []

# Main function to collect details asynchronously
async def extract_movie_lists(year):
    base_url = "https://www.imdb.com/search/title/"
    genre_list = ["action", "adventure", "animation", "biography", "comedy", "crime", "family", "fantasy", "history",
                  "horror", "music", "musical", "mystery", "romance", "sport", "thriller", "war", "western"]
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36'}
    all_movies_data = []

    async with aiohttp.ClientSession() as session:
        tasks = []
        for each_genre in genre_list:
            params = {
                "title_type": "feature",
                "release_date": f"{year}-01-01,{year}-12-31",
                "genres": each_genre
            }
            tasks.append(fetch_movie_lists_data(session, base_url, params, headers, each_genre))

        # Run all tasks concurrently
        results = await asyncio.gather(*tasks)

        # Flatten the list of lists
        for movie_list in results:
            all_movies_data.extend(movie_list)

    # Create a DataFrame from the collected data
    df = pd.DataFrame(data=all_movies_data)
    df_cleaned = df.drop_duplicates(subset="imdb_id", keep='first')

    return df_cleaned
