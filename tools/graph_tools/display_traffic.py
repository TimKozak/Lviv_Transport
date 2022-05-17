# Alina

import folium
import folium.plugins as plugins
from retrieve_traffic import get_info
from retrieve_routes import retrieve_routes

def display_traffic(datalist, map):
    coords = []

    for data in datalist:
        clear_data = data['flowSegmentData']['coordinates']
        coord_location = clear_data['coordinate']

        for elem in coord_location:
            latlon = (elem['latitude'], elem['longitude'])
            coords.append(latlon)

    plugins.HeatMap(coords, radius=10, use_local_extrema=True).add_to(map)


if __name__ == '__main__':
    map = folium.Map(location=(49.8397, 24.0297), zoom_start=12) #Lviv
    folium.TileLayer('cartodbdark_matter').add_to(map)

    retrieved_routes, route_names = retrieve_routes()
    datalist = []

    for point in retrieved_routes[0]:
        data = get_info(point)
        datalist.append(data)

    display_traffic(datalist, map)
    	
    folium.PolyLine(retrieved_routes[0], color="#cc2299", weight=2.5, opacity=1).add_to(map)

    map.add_child(folium.LayerControl())
    map.save('map.html')
