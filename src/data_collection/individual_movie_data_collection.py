import aiohttp
import asyncio
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import random

# Function to fetch movie details asynchronously
async def fetch_individual_movie_data(session, imdb_id):
    url = f"https://www.imdb.com/title/{imdb_id}/"
    #headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36'}
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9',
        'Referer': 'https://www.imdb.com/'
    }
    #print(f"Fetching data for IMDb ID: {imdb_id}")
    try:
        await asyncio.sleep(random.uniform(1, 5))

        timeout = aiohttp.ClientTimeout(total=20)
        async with session.get(url, headers=headers, timeout = timeout) as response:
            content = await response.text()
            soup = BeautifulSoup(content, "html.parser")

            # Extract actors (first 3)
            actors = []
            actor_tags = soup.find_all('a', {'data-testid': 'title-cast-item__actor'})
            if actor_tags:
                for actor_tag in actor_tags[:3]:  # Limit to first 3 actors
                    actors.append(actor_tag.text.strip())  # Add actor name to the list
            else:
                actors = np.nan  # Use np.nan for missing values

            # Extract director (first one)
            director_name = np.nan  # Default value
            director_tags = soup.find_all('a', class_="ipc-metadata-list-item__list-content-item ipc-metadata-list-item__list-content-item--link")
            if director_tags:
                director_name = director_tags[0].text.strip()  # Take the first director

            # Extract budget
            budget_value = np.nan  # Default value
            budget_element = soup.find('li', {'data-testid': 'title-boxoffice-budget'})
            if budget_element:
                budget_value = budget_element.find('span', class_="ipc-metadata-list-item__list-content-item").text.strip()

            # Extract gross worldwide
            gross_value = np.nan  # Default value
            gross_element = soup.find('li', {'data-testid': 'title-boxoffice-cumulativeworldwidegross'})
            if gross_element:
                gross_value = gross_element.find('span', class_="ipc-metadata-list-item__list-content-item").text.strip()

            # Return the data as a dictionary
            return {
                "imdb_id": imdb_id,
                "actors": actors,
                "director": director_name,
                "budget": budget_value,
                "worldwide_gross": gross_value
            }

    except Exception as e:
        print(f"Error fetching data for IMDb ID {imdb_id}: {e}")
        return {
            "imdb_id": imdb_id,
            "actors": np.nan,
            "director": np.nan,
            "budget": np.nan,
            "worldwide_gross": np.nan
        }





async def extract_individual_movies(df):
    all_movie_data = []

    async with aiohttp.ClientSession() as session:
        tasks = [fetch_individual_movie_data(session, imdb_id) for imdb_id in df['imdb_id']]
        results = await asyncio.gather(*tasks)

        for result in results:
            all_movie_data.append(result)

    # Create a DataFrame from the collected data
    new_data_df = pd.DataFrame(data=all_movie_data)

    # # Merge the new data with the existing DataFrame based on 'imdb_id'
    # df_updated = df.merge(new_data_df, on='imdb_id', how='left')

    return new_data_df
