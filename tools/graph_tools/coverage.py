# display coverage with folium

import folium
from retrieve_routes import retrieve_routes 

def display_coverage(mins):
    routes, names = retrieve_routes()
    coords = [elem for route in routes for elem in route]

    map = folium.Map(location=(49.8397, 24.0297), zoom_start=12) #Lviv

    for i in range(len(coords)):
        lat, lon = coords[i]

        folium.Circle([lat, lon],
                        radius=75*mins, #100 metres per minute
                        color='#3186cd',
                        fill_color='#3186cd',
                        opacity=0.5,
                        fill_opacity=0.3
                    ).add_to(map)
 
    map.add_child(folium.LayerControl())
    map.save('map.html')


if __name__ == '__main__':
    display_coverage(mins=3)

