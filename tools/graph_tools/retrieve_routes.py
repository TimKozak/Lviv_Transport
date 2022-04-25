from asyncio import current_task
import json

def retrieve_routes():
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