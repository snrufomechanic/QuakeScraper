from datetime import datetime
import requests

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
