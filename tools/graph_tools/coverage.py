# Alina
import folium
from retrieve_routes import retrieve_routes
import folium.plugins as plugins

def display_coverage(routes, central_point, radius):
    '''
    Generate a folium map, depicting coverage of the city with public transport stops.

    Args:
        routes: list
            list of all public transport routes
        central_point: tuple(float, float)
            the coordinates of the point where the map will open at first
        radius: int
            radius of every "point" on the map
    '''
    coords = [elem for route in routes for elem in route]

    map = folium.Map(location=central_point, zoom_start=12)
    plugins.HeatMap(coords, radius=radius, use_local_extrema=True).add_to(map)
    map.add_child(folium.LayerControl())
    map.save('././images/coverage_map.html')

if __name__ == '__main__':
    routes, names = retrieve_routes()
    display_coverage(routes, central_point=(49.8397, 24.0297), radius=10)

