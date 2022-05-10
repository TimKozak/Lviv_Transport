# Alina
import json

def retrieve_routes() -> list:
    '''
    Form list of routes from a json file.

    Returns:
        retrieved_routes: list[list[tuple()]]
            list of routes, each route defined as [(stop1, stop2), (stop1, stop3)],
            where each stop is defined as (lat, lon)
        route_names: list[list[str]]
            list of routes, each route defines as a list of the names of
            public transport stops
    '''
    with open('./jsons/shapes_routes.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    retrieved_routes = []
    route_names = []

    for key in data.keys():
        route_stops = []
        current_stations = data[key]
    
        for station in current_stations:
            st_coords = (float(station[0]), float(station[1]))
            route_stops.append(st_coords)
        
        retrieved_routes.append(route_stops)
        route_names.append(key)

    return retrieved_routes, route_names
