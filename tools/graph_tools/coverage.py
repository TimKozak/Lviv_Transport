# Alina
import folium
from retrieve_routes import retrieve_routes
import folium.plugins as plugins

def display_coverage():
    '''
    Generate a folium map, depicting coverage of the city with public transport stops.
    '''
    routes, names = retrieve_routes()
    coords = [elem for route in routes for elem in route]

    map = folium.Map(location=(49.8397, 24.0297), zoom_start=12) #Lviv
    plugins.HeatMap(coords, radius=10, use_local_extrema=True).add_to(map)


if __name__ == '__main__':
    display_coverage()

