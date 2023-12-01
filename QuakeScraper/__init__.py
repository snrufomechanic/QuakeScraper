import time

import requests
import json
import os
import pandas as pd
import folium
from folium import Popup, Html
from folium.plugins import MarkerCluster, FloatImage


def fetch_earthquake_data(start_year, start_month, start_day, end_year, end_month, end_day,
                          min_latitude=35.00, max_latitude=42.00, min_longitude=26.00, max_longitude=45.00,
                          min_magnitude=3.5, max_magnitude=9.0, min_depth=0, max_depth=500, output_type='DF'):
    print(
        "\nBu paket ile alacağınız her türlü veriyi, haritayı ve bilgiyi Telif Hakları Yasası gereğince... \nT.C. "
        "İçişleri Bakanlığı Afet ve Acil Durum Yönetimi Başkanlığı Deprem Dairesi Başkanlığı'nı kaynak göstererek "
        "kullanmanız gerekmektedir.")
    print("\n\nŞartları kabul ediyorsanız devam etmek için E, Çıkış için H komutu kullanabilirsiniz.")
    user_input = input("Devam Etmek istiyor musunuz? (e/H): ")
    if user_input.lower() == 'e':
        print("Veri alınıyor.")
        base_url = "https://deprem.afad.gov.tr/EventData/GetEventsByFilter"

        headers = {
            "accept": "application/json, text/plain, */*",
            "accept-language": "tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7,pt;q=0.6",
            "cache-control": "no-cache, no-store, must-revalidate",
            "content-type": "application/json",
            "sec-ch-ua": "\"Google Chrome\";v=\"119\", \"Chromium\";v=\"119\", \"Not?A_Brand\";v=\"24\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\"",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "strict-transport-security": "max-age=16070400; includeSubDomains",
            "x-content-type-options": "nosniff",
            "x-frame-options": "deny",
            "x-xss-protectio": "1; mode=block",
            "credentials": "include"
        }

        payload = {
            "EventSearchFilterList": [
                {"FilterType": 1, "Value": str(min_latitude)},
                {"FilterType": 2, "Value": str(max_latitude)},
                {"FilterType": 3, "Value": str(min_longitude)},
                {"FilterType": 4, "Value": str(max_longitude)},
                {"FilterType": 7, "Value": str(max_depth)},
                {"FilterType": 11, "Value": str(min_magnitude)},
                {"FilterType": 12, "Value": str(max_magnitude)},
                {"FilterType": 8, "Value": f"{start_year}-{start_month}-{start_day}T00:00:00.000Z"},
                {"FilterType": 9, "Value": f"{end_year}-{end_month}-{end_day}T23:59:59.999Z"}
            ],
            "Skip": 0,
            "take": 999999,
            "SortDescriptor": {"field": "eventDate", "dir": "desc"}
        }

        response = requests.post(base_url, headers=headers, data=json.dumps(payload))
        result = response.json()

        if output_type == 'DF':
            # Assuming result is a list of dictionaries, you may need to adjust this based on the actual structure
            dataframe = pd.DataFrame(result)
            return event_list_parser(dataframe)

        elif output_type == 'TXT':
            # Assuming you want to save the JSON response as text
            try:
                os.makedirs(os.path.join(os.getcwd(), 'output/TXT'), exist_ok=True)

                output_path = os.path.join(os.getcwd(),
                                           f"output/TXT/{start_year}-{start_month}-{start_day}-{end_year}-{end_month}-{end_day}-{min_magnitude}-{max_magnitude}.txt")
                with open(output_path, 'w') as txt_file:
                    json.dump(result, txt_file)
                print(f'Data Successfully saved to text file. path:"{output_path}"')
                return True

            except Exception as e:
                print(f"Error saving to text file: {e}")
                return False

        elif output_type == 'CSV':
            # Convert the JSON response to a DataFrame and save as CSV
            try:
                os.makedirs(os.path.join(os.getcwd(), 'output/CSV'), exist_ok=True)
                output_path = os.path.join(os.getcwd(),
                                           f'output/CSV/{start_year}-{start_month}-{start_day}-{end_year}-{end_month}-{end_day}-{min_magnitude}-{max_magnitude}.csv')
                dataframe = pd.DataFrame(result)
                dataframe.to_csv(output_path, index=False)
                print(f'Data Successfully saved to CSV file. path:"{output_path}"')
                return True
            except Exception as e:
                print(f"Error saving to CSV file: {e}")
                return False

        else:
            raise ValueError("Invalid output type. Must be 'DF', 'TXT', or 'CSV'.")
    else:
        print("Kulllanım şartlarını kabul etmediniz. Çıkış yapılıyor.")
        for sec in range(0, 6):
            time.sleep(1)

        exit()


def event_list_parser(dataframe):
    return pd.json_normalize(dataframe['eventList'])


def create_map_image(parsed_event_list):
    """
    Create a Folium map with CircleMarkers for earthquake events.

    Parameters:
    - parsed_event_list (pd.DataFrame): DataFrame containing earthquake event data.

    Returns:
    - folium.Map: The generated Folium map.
    """
    print("Harita oluşturuluyor.")
    # Create a base map

    earthquake_map = folium.Map(location=[parsed_event_list['latitude'].mean(), parsed_event_list['longitude'].mean()],
                                zoom_start=5, control_scale=True)
    url = "https://www.afad.gov.tr/kurumlar/afad.gov.tr/Kurumsal-Kimlik/Logolar/PNG/AFAD-_-Icisleri-Bkn.png"
    logo = FloatImage(image=url, bottom=1, left=1, width='25%')
    logo.add_to(earthquake_map)

    # Create a MarkerCluster layer for better performance
    marker_cluster = MarkerCluster().add_to(earthquake_map)

    # Add markers to the map
    for index, row in parsed_event_list.iterrows():
        popup_html = Html(f'<table><thead><thead><tbody></tbody></table><a href="https://deprem.afad.gov.tr/event-detail/{row["id"]}">Detaylar</a>', script=True)
        popup = Popup(popup_html, max_width=300)
        folium.CircleMarker(
            location=[row['latitude'], row['longitude']],
            radius=row['magnitude'] * 2,  # Adjust the multiplier as needed
            color='red' if row['magnitude'] > 5.5 else ('yellow' if row['magnitude'] > 3.5 else 'green'),
            fill=True,
            fill_color='red' if row['magnitude'] > 5.5 else ('yellow' if row['magnitude'] > 3.5 else 'green'),
            fill_opacity=0.6,
            tooltip=f"{row['magnitude']}",
            popup=popup
        ).add_to(marker_cluster)

    # Save the map as an HTML file
    output_dir = 'output/'
    os.makedirs(output_dir, exist_ok=True)
    output_path = 'output/map.html'
    earthquake_map.save(output_path)
    print(f'Map successfully saved. Path: "{output_path}"')
    return earthquake_map
