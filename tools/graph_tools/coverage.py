# display coverage with folium

import folium
from retrieve_routes import retrieve_routes 

def display_coverage(mins):
    odd_routes, odd_names, even_routes, even_names = retrieve_routes()
    odd_coords = [elem for route in odd_routes for elem in route]
    even_coords = [elem for route in even_routes for elem in route]

    map = folium.Map(location=(49.8397, 24.0297), zoom_start=12) #Lviv

    for i in range(len(odd_coords)):
        lat, lon = odd_coords[i]

        folium.Circle([lat, lon],
                        radius=75*mins, #100 metres per minute
                        color='#3186cd',
                        fill_color='#3186cc',
                        opacity=0.5,
                        fill_opacity=0.3
                    ).add_to(map)
 
    for i in range(len(even_coords)):
        lat, lon = even_coords[i]

        folium.Circle([lat, lon],
                        radius=75*mins, #100 metres per minute
                        color = '#cd3186',
                        fill_color='#cc3186',
                        opacity=0.5,
                        fill_opacity=0.3
                    ).add_to(map)
 
    map.add_child(folium.LayerControl())
    map.save('map.html')


if __name__ == '__main__':
    display_coverage(mins=3)

