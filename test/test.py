from QuakeScraper import fetch_earthquake_data




if __name__ == "__main__":
    data = fetch_earthquake_data(
        start_year="2022",
        start_month="11",
        start_day="23",
        end_year="2023",
        end_month="11",
        end_day="23",
        output_type='DF'
    )
    print(data)
