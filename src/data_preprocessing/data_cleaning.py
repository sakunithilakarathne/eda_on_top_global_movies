import pandas as pd
import numpy as np

dataset = pd.read_csv("")
# Understanding the size of the dataset
print(dataset.shape)

# Understanding the columns
print(dataset.columns)

# Checking for duplicate data

duplicates = dataset[dataset.duplicated(subset='imdb_id', keep=False)]
print(duplicates.shape)

# Checking for missing values

dataset.isnull().sum()

# Understanding the missing value percentage of each column

dataset.isnull().mean() *100

#Handling the missing values
# Budget is missing in more than 50% of rows. Since this is too high column is dropped
dataset.drop(columns=['budget'], inplace=True)

# imdb id represents a similar value to meta score. Therefore, dropping the meta score column
dataset.drop(columns=['metascore'], inplace=True)

# Filling categorical columns with Unknown placeholder
dataset['actors'].fillna('Unknown', inplace=True)
dataset['director'].fillna('Unknown', inplace=True)

# Fill missing month with the most common month
dataset['release_month'].fillna(dataset['release_month'].mode()[0], inplace=True)

# Filling runtime with the mean value
dataset['runtime'].fillna(dataset['runtime'].median(), inplace=True)

# Removing $ prefix and . from Domestic Gross column
dataset["worldwide_gross"] = dataset["worldwide_gross"].str.replace("$", "")
dataset["worldwide_gross"] = dataset["worldwide_gross"].str.replace(",", "")

dataset['worldwide_gross'] = pd.to_numeric(dataset['worldwide_gross'], errors='coerce')


# Imputing worldwide_gross with mean of respective genre
genre_mean_dict = dataset.groupby('each_genre')['worldwide_gross'].mean().to_dict()
# Step 3: Define a function to impute missing values based on genre
def impute_worldwide_gross(row):
    if pd.isna(row['worldwide_gross']):  # Check if worldwide_gross is missing
        return genre_mean_dict.get(row['each_genre'], np.nan)  # Use genre mean or NaN if genre not found
    return row['worldwide_gross']  # Return original value if not missing

# Step 4: Apply the function to impute missing values
dataset['worldwide_gross'] = dataset.apply(impute_worldwide_gross, axis=1)

# Step 6: Convert worldwide_gross to integers (optional)
dataset['worldwide_gross'] = dataset['worldwide_gross'].astype(int)
# Convert month into int type
dataset['release_month'] = dataset['release_month'].astype(int)
# Convert runtime from seconds into minutes
dataset['runtime'] = dataset['runtime']/60
# Convert runtime into int
dataset['runtime'] = dataset['runtime'].astype(int)