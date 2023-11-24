# Earthquake Scraper

## A Python package for scraping earthquake data from [Kandilli Observatory and Earthquake Research Institute (KOERI)](http://www.koeri.boun.edu.tr/) and extracting useful information.

# -Installation

---

```bash
pip install QuakeScraper
```

---

## <h1> Usage </h1>

```python
# Example usage of the earthquake scraper

from QuakeScraper_snrufomechanic.earthquake_scraper import fetch_earthquake_data

# Define your query parameters

start_year = "2023"
start_month = "01"
start_day = "01"
end_year = "2023"
end_month = "12"
end_day = "31"

# Fetch earthquake data and save as a DataFrame

earthquake_df = fetch_earthquake_data(start_year, start_month, start_day, end_year, end_month, end_day, output_type='DF')

# Display the DataFrame

print(earthquake_df.head())
```

---

<h1> Parameters </h1>
- start_year, start_month, start_day: Start date of the query period. <br>
- end_year, end_month, end_day: End date of the query period. <br>
- Other optional parameters for specifying the geographical area, earthquake  magnitude, depth, and output type.

---

<h1> Output Types </h1>
DF: Returns the earthquake data as a DataFrame.
TXT: Saves the raw data to a text file.
CSV: Converts the raw data to CSV format and saves it to a file.
