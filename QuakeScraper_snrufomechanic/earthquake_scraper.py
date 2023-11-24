# script/earthquake_scraper.py
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd
import io


def generate_ofname_parameter(yyyy1, mm1, dd1, yyyy2, mm2, dd2, mag1, mag2):
    # Get the current date and time components
    now = datetime.now()
    sec = now.second
    msec = now.microsecond // 1000

    # Generate the dynamic filename
    fname = f"{yyyy1}{mm1}{dd1}_{yyyy2}{mm2}{dd2}_{mag1}_{mag2}_{sec}_{msec}.txt"

    # Replace invalid characters
    fname = fname.replace(",", ".")
    fname = fname.replace(":", ".")
    fname = fname.replace(";", ".")
    fname = fname.replace("/", ".")

    return fname


def fetch_earthquake_data(start_year, start_month, start_day, end_year, end_month, end_day,
                          min_latitude=35.00, max_latitude=42.00, min_longitude=26.00, max_longitude=45.00,
                          min_magnitude=3.5, max_magnitude=9.0, min_depth=0, max_depth=500, output_type='DF'):
    """
    Fetch earthquake data from the specified source.

    Parameters:
    - start_year (str): The start year of the query period.
    - start_month (str): The start month of the query period.
    - start_day (str): The start day of the query period.
    - end_year (str): The end year of the query period.
    - end_month (str): The end month of the query period.
    - end_day (str): The end day of the query period.
    - min_latitude (float): The minimum latitude of the geographical area.
    - max_latitude (float): The maximum latitude of the geographical area.
    - min_longitude (float): The minimum longitude of the geographical area.
    - max_longitude (float): The maximum longitude of the geographical area.
    - min_magnitude (float): The minimum earthquake magnitude.
    - max_magnitude (float): The maximum earthquake magnitude.
    - min_depth (int): The minimum earthquake depth.
    - max_depth (int): The maximum earthquake depth.
    - output_type (str): The output type of the data. Can be 'DF' (default) or 'TXT' or 'CSV'.

    Returns:
    - DataFrame or str: The earthquake data as a DataFrame or text content.
    """

    base_url = "http://www.koeri.boun.edu.tr/sismo/zeqdb/submitRecSearchT.asp"

    url_params = {
        "bYear": start_year,
        "bMont": start_month,
        "bDay": start_day,
        "eYear": end_year,
        "eMont": end_month,
        "eDay": end_day,
        "EnMin": min_latitude,
        "EnMax": max_latitude,
        "BoyMin": min_longitude,
        "BoyMax": max_longitude,
        "MAGMin": min_magnitude,
        "MAGMax": max_magnitude,
        "DerMin": min_depth,
        "DerMax": max_depth,
        "Tip": "Deprem",
        "ofName": generate_ofname_parameter(start_year, start_month, start_day, end_year, end_month, end_day,
                                            min_magnitude, max_magnitude),
    }

    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,"
                  "application/signed-exchange;v=b3;q=0.7",
        "accept-language": "tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7,pt;q=0.6",
        "upgrade-insecure-requests": "1"
    }

    response = requests.get(base_url, params=url_params, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find name holder textbox by id. id = boxFNAMEphs
    file_name = soup.find(id='boxFNAME').get('value')
    if file_name is None:
        raise Exception("File name holder not found.")
    else:
        raw_data_txt = download_file(file_name)

        if output_type == 'DF':
            # Parse the raw data into a DataFrame
            dataframe = pd.read_csv(io.StringIO(raw_data_txt), delimiter="\t")
            return dataframe

        elif output_type == 'TXT':
            try:

                output_path = f"./output/TXT/{file_name}"
                with open(output_path, 'w') as txt_file:
                    txt_file.write(raw_data_txt)
                print(f'Data Successfully saved to text file. path:"./output/TXT/{file_name} "')
                return True

            except Exception as e:

                print(f"Error saving to text file: {e}")
                return False  # Failed to save to text file

        elif output_type == 'CSV':
            # Convert the raw data to CSV format and save ./output/CSV/{filename} folder.
            raise ValueError("BURASI YAPILIR Bİ ARA^^.")

        else:
            raise ValueError("Invalid output type. Must be 'DF', 'TXT', or 'CSV'.")


def download_file(file_name):
    """
    Download the file with the specified name.

    Parameters:
    - file_name (str): The name of the file to download.

    Returns:
    - str: The text content of the downloaded file.
    """
    base_url = "http://www.koeri.boun.edu.tr/sismo/zeqdb/download.php?download_file="
    url = base_url + file_name
    response = requests.get(url)
    return response.text
