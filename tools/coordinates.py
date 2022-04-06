import requests
import pandas as pd


API_KEY = "f7cb5dee9b722bfb02d5bd4e6b3d3996"
URL = f"http://api.positionstack.com/v1/forward"


def read_file():
    with open("./no_coord_stations.txt", "r", encoding="utf-8") as file:
        no_geo_stations = file.readlines()
        no_geo_stations = [adr[:-1] for adr in no_geo_stations]

    return no_geo_stations


def get_geo_information(stations):
    geo_information_arr = []
    for station in stations:
        response = requests.get(
            f"{URL}?access_key={API_KEY}&query=м. Львів, {station}"
        ).json()

        if response["data"]:
            geo_information = response["data"][0]
            print(geo_information)
            coordinates = [
                station,
                geo_information["latitude"],
                geo_information["longitude"],
            ]
            print(coordinates)
            geo_information_arr.append(coordinates)
        else:
            geo_information_arr.append([station, "", ""])

    return geo_information_arr


def write_csv(data):
    columns = ["station", "latitude", "longitude"]
    df = pd.DataFrame(data, columns=columns)
    df.to_csv("./data/missed_geo_information.csv")


if __name__ == "__main__":
    stations = read_file()
    geo_information = get_geo_information(stations)
    write_csv(geo_information)
