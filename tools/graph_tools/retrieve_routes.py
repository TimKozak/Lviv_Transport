# Alina

import json

def retrieve_routes() -> tuple:
    """
    Retrievs data from shapes_routes.json and returns the tuple of routes and their names.
    """
    with open('./jsons/shapes_routes.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # make list of tuples: [(stop1, stop2), (stop1, stop3)]
    # each stop: (lat, lon)

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

if __name__ == '__main__':
    routes, names = retrieve_routes()
    stations = []

    for route in routes:
        for station in route:
            stations.append(station)
    
    print(len(routes))

