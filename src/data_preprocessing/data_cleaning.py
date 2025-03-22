import pandas as pd
import numpy as np


def removing_duplicates(dataset):
    """
    Checks for the missing values in dataset and removes them.
    """
    # Check for duplicates
    duplicates = dataset.duplicated(subset='imdb_id', keep=False)
    duplicate_rows = dataset[duplicates]

    # Check if there are any duplicates
    if duplicate_rows.empty:
        print("\n No Duplicates found !\n")
    else:
        print("Duplicates found:")
        dataset.drop_duplicates(subset=['IMDb ID'], keep='first', inplace=True)
        print("Duplicated Removed")

    return dataset


def clean_dataset(dataset):
    """
    Handles missing values through imputation, drops unnecessary columns
    and convert data types.
    Input Parameter - dataset to be cleaned
    Returns - cleaned dataset
    """

    # Drop unnecessary columns
    dataset.drop(columns=['budget', 'metascore'], inplace=True)

    # Fill categorical columns with 'Unknown'
    dataset['actors'].fillna('Unknown', inplace=True)
    dataset['director'].fillna('Unknown', inplace=True)

    # Fill missing release_month with the most common month
    dataset['release_month'].fillna(dataset['release_month'].mode()[0], inplace=True)

    # Fill runtime with the median value
    dataset['runtime'].fillna(dataset['runtime'].median(), inplace=True)

    # Clean and convert worldwide_gross to numeric
    dataset["worldwide_gross"] = dataset["worldwide_gross"].str.replace("$", "")
    dataset["worldwide_gross"] = dataset["worldwide_gross"].str.replace(",", "")
    dataset['worldwide_gross'] = pd.to_numeric(dataset['worldwide_gross'], errors='coerce')

    # Impute worldwide_gross with mean of respective genre
    genre_mean_dict = dataset.groupby('each_genre')['worldwide_gross'].mean().to_dict()

    def impute_worldwide_gross(row):
        if pd.isna(row['worldwide_gross']):
            return genre_mean_dict.get(row['each_genre'], np.nan)
        return row['worldwide_gross']

    dataset['worldwide_gross'] = dataset.apply(impute_worldwide_gross, axis=1)

    # Convert worldwide_gross to integers
    dataset['worldwide_gross'] = dataset['worldwide_gross'].astype(int)

    # Convert release_month to int
    dataset['release_month'] = dataset['release_month'].astype(int)

    # Convert runtime from seconds to minutes and then to int
    dataset['runtime'] = dataset['runtime'] / 60
    dataset['runtime'] = dataset['runtime'].astype(int)

    return dataset