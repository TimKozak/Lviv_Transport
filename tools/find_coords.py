import requests
import pandas as pd

URL = f"https://nominatim.openstreetmap.org/search"

def read_file():
    with open("./no_coord_stations.txt", "r", encoding="utf-8") as file:
        no_geo_stations = file.readlines()

        for i, line in enumerate(no_geo_stations):
                if '(' in line: no_geo_stations[i] = line[line.index('.')+1:line.index('(')]
                elif '.' in line: no_geo_stations[i] = line[line.index('.')+1:-1]
                else: no_geo_stations[i] = line[:-1]

        for i, line in enumerate(no_geo_stations):
            if '.' in line: no_geo_stations[i] = line[line.index('.')+1:]

    return no_geo_stations


def get_geo_information(stations):
    geo_info = []
    for station in stations:
        params = {'street': station, 'city': 'Львів', 'format': 'json'}
        request_result = requests.get(URL, params=params)
        js_result = request_result.json()

        try:
            geo_info.append([station, js_result[0]['lat'], js_result[0]['lon']])
        except IndexError:
            geo_info.append([station, "", ""])

    return geo_info


def write_csv(data):
    columns = ["station", "latitude", "longitude"]
    df = pd.DataFrame(data, columns=columns)
    df.to_csv("missed_geo_information.csv")


if __name__ == "__main__":
    stations = read_file()
    geo_information = get_geo_information(stations)
    write_csv(geo_information)
