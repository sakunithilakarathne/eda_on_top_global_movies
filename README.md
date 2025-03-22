# Movie Data Analysis (2000-2020)

This project analyzes movie data collected from the IMDb website for the years 2000 to 2020. The dataset includes details such as IMDb ID, title, genre, ratings, runtime, release information, actors, directors, language, and country. The analysis focuses on data preprocessing, statistical insights, visualization, and trends in movie genres, directors, and revenue.

---

## Data Collection and Preprocessing
- Data was scraped from IMDb's Advanced Title Search page and individual movie pages using web scraping techniques.
- Key columns collected: IMDb ID, title, genre, meta score, IMDb rating, vote count, release year, release month, runtime, actors, director, language, and country.
- Missing values were handled by:
  - Dropping the budget column (over 50% missing).
  - Imputing categorical columns with mode or "Unknown."
  - Filling numerical columns with mean/median values.
- Worldwide gross values were cleaned (removed symbols) and imputed based on genre-specific means.

---

## Challenges
- Web scraping was slow due to the need to scrape individual movie pages. Solutions like IMDb API or asynchronous requests were considered.
- Missing data in worldwide gross and meta score columns required careful imputation based on genre and country.

---

## Tools and Techniques
- **Python Libraries**: Pandas, NumPy, Matplotlib, Seaborn.
- **Web Scraping**: BeautifulSoup, Requests.
- **Data Cleaning**: Handling missing values, data type conversion.
- **Visualization**: Distribution plots, boxplots, bar charts.
- **Statistical Analysis**: Descriptive statistics, correlation analysis.

---

## Conclusion
This analysis provides valuable insights into movie trends, genre popularity, and the impact of directors and actors on movie success. It highlights the dominance of action and adventure genres, the influence of holiday seasons on movie revenue, and the importance of IMDb ratings and vote counts in determining a movie's popularity.

---
