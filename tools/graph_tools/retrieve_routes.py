from asyncio import current_task
import json

def retrieve_routes():
    with open('./jsons/routes.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    # make list of tuples: [(stop1, stop2), (stop1, stop3)]
    # each stop: (lat, lon)

    retrieved_even_routes = []
    retrieved_odd_routes = []
    even_route_names = []
    odd_route_names = []

    for key in data.keys():
        odd = True if 'odd' in key else False
        route_stops = []
        current_route = data[key]
        current_stations = current_route['stations']

        for station in current_stations:
            st_coords = tuple(station['coords'])
            route_stops.append(st_coords)

        if odd:
            retrieved_odd_routes.append(route_stops)
            odd_route_names.append(key)
        else:
            retrieved_even_routes.append(route_stops)
            even_route_names.append(key)
    
    return retrieved_odd_routes, odd_route_names, retrieved_even_routes, even_route_names

# odd_routes, odd_names, even_routes, even_names = retrieve_routes()

