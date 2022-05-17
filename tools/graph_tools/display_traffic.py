# Alina
import folium
import folium.plugins as plugins
from retrieve_traffic import get_info
from retrieve_routes import retrieve_routes

def display_traffic(datalist: list, map):
    '''
    Display traffic based on traffic points from <datalist> on the folium map <map>.

    Args:
        datalist: list
            list of routes (each one is list of points)
        map: folium.Map
            folium map for displaying the traffic
    '''
    coords = []

    for data in datalist:
        clear_data = data['flowSegmentData']['coordinates']
        coord_location = clear_data['coordinate']

        for elem in coord_location:
            latlon = (elem['latitude'], elem['longitude'])
            coords.append(latlon)

    plugins.HeatMap(coords, radius=10, use_local_extrema=True).add_to(map)

def generate_map(n: int):
    '''
    Generate a folium map, depicting coverage of the city with traffic, based
    on the coordinates of the public transport stops of each route.

    Parameters:
        n: int
            number of routes to take points from
    '''
    map = folium.Map(location=(49.8397, 24.0297), zoom_start=12) #Lviv
    folium.TileLayer('cartodbdark_matter').add_to(map)

    retrieved_routes, route_names = retrieve_routes()
    datalist = []

    for route in retrieved_routes[:n]:
        for point in route: # take only 1st route for demonstration
            data = get_info(point)
            datalist.append(data)

    display_traffic(datalist, map)
    	
    folium.PolyLine(retrieved_routes[0], color="#cc2299", weight=2.5, opacity=1).add_to(map)

    map.add_child(folium.LayerControl())
    map.save('map.html')


if __name__ == '__main__':
    generate_map(1)