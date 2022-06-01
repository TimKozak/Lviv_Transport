import numpy as np
import pandas as pd

def haversine_np(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)

    All args must be of equal length.    

    """
    lon1, lat1, lon2, lat2 = map(np.radians, [lon1, lat1, lon2, lat2])

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = np.sin(dlat/2.0)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2.0)**2

    c = 2 * np.arcsin(np.sqrt(a))
    km = 6367 * c
    return km

def add_distance_and_district(changes_file_route, district_file_route):
    """Add a distance and a district columns for route_changes.csv"""

    df = pd.read_csv(changes_file_route)

    df['distance'] = haversine_np(df['from_long'], df['from_lat'], df['to_long'], df['to_lat'])
    
    df['to_lat'] = round(df['to_lat'], 4)
    df['to_long'] = round(df['to_long'], 4)
    df['from_lat'] = round(df['from_lat'], 4)
    df['from_long'] = round(df['from_long'], 4)

    district_df = pd.read_csv(district_file_route)[['latitude', 'longitude', 'district']]
    district_df['latitude'] = round(district_df['latitude'], 4)
    district_df['longitude'] = round(district_df['longitude'], 4)
    district_df.columns = ['to_lat', 'to_long', 'to_district']

    print(district_df)

    print(df.dtypes)

    new_df = pd.merge(district_df, df,  on='to_lat', how='left')

    district_df.columns = ['from_lat', 'from_long', 'from_district']
    new_df = pd.merge(district_df, new_df, on='from_lat', how='left')

    new_df.to_csv("./data/route_changes_districts.csv")

if __name__ == "__main__":
    add_distance_and_district('./data/route_changes.csv', './data/stations.csv')