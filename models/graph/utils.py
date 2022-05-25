from numpy import arcsin, cos, deg2rad, sin, sqrt

from location import Location
from node import StationNode

LVIV_LAT, LVIV_LON = 49.8425, 24.032222


def get_len_of_lon_lat(lat=LVIV_LAT, lon=LVIV_LON, unit_size=0.1):
    """
    calculates the unit size of lattide and longtitude in given region
    To be used only in regions of city - small country size
    """
    new_lat, new_lon = lat + unit_size, lon + unit_size

    r = 6378.8
    lat, lon, new_lat, new_lon = deg2rad([lat, lon, new_lat, new_lon]).astype("float")

    dlat1 = new_lat - lat
    dlon1 = 0

    dlat2 = 0
    dlon2 = new_lon - lon

    a1 = (
        sin(dlat1 / 2) ** 2 + cos(new_lat) * cos(lat) * sin(dlon1 / 2) ** 2
    )  # dist between lat, lat + 0.1
    a2 = (
        sin(dlat2 / 2) ** 2 + cos(lat) * cos(lat) * sin(dlon2 / 2) ** 2
    )  # dist between lon, lon + 0.1

    c1 = 2 * arcsin(sqrt(a1))
    c2 = 2 * arcsin(sqrt(a2))

    d1, d2 = c1 * r, c2 * r
    return d1, d2, unit_size


LAT_UNIT_DIST, LON_UNIT_DIST, UNIT_SIZE = get_len_of_lon_lat()


def lat_lon2km(
    stations: list, lat_unit=LAT_UNIT_DIST, lon_unit=LON_UNIT_DIST, unit_size=0.1
):
    """
    transforms latitude and longtitude into kilometers using estimated
    unit length of lat and lon on given location.
    To be used only in regions of city - small country size
    """
    stations_km = list()

    for st in stations:
        lat, lon = st.location.lat, st.location.lon
        lat_km, lon_km = lat * lat_unit / unit_size, lon * lon_unit / unit_size
        new_st = StationNode(Location(lat_km, lon_km), st.name)
        stations_km.append(new_st)

    return stations_km
