from nbformat import write
import pandas as pd


def read_csv_file(path_to_file):
    df = pd.read_csv(path_to_file)
    return df


def fill_missed_information(df_missed_geo, df_stations):
    def find_matching_coords(street):
        matching_row = df_missed_geo[df_missed_geo["street"] == street].iloc[0]
        return (matching_row["latitude"], matching_row["longitude"])

    for ind, row in df_stations.iterrows():
        if pd.isna(row["latitude"]) or pd.isna(row["longitude"]):
            coords = find_matching_coords(row["street"])
            df_stations.at[ind, "latitude"] = coords[0]
            df_stations.at[ind, "longitude"] = coords[1]

    return df_stations


def write_csv_file(df_result, path_to_file):
    df_result.to_csv(path_to_file, index=False)


if __name__ == "__main__":
    df_missed_geo = read_csv_file("./data/missed_geo_information.csv")
    df_stations = read_csv_file("./data/stations.csv")
    df_result = fill_missed_information(df_missed_geo, df_stations)
    write_csv_file(df_result, "./data/stations_filled_geo.csv")
