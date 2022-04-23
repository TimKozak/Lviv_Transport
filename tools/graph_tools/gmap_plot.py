import gmplot 
import json

# Load file data
with open('./shapes_routes.json', 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)

# Define GmapOne with starting coords and zoom value
gmapOne = gmplot.GoogleMapPlotter(49.84063, 24.02868, 15)

# Iterate through every route
for route in data.items():

    # Create separate arrays of latitudes, longitudes and names
    lats = [float(elem[0]) for elem in route[1]]
    lons = [float(elem[1]) for elem in route[1]]
    names = [str(elem[3]) for elem in route[1] if elem]

    # Filter separately for stations
    station_lats = []
    station_lons = []
    station_names = []
    for i in range(len(names)):
        if names[i] != 'None':
            station_lats.append(lats[i])
            station_lons.append(lons[i])
            station_names.append(names[i])

    # Plot routes
    gmapOne.scatter(lats, lons, 'blue', size=2.5, marker=False)
    gmapOne.plot(lats, lons, 'blue', edge_width=2.5)

    # Plot stations with names
    # gmapOne.scatter(station_lats, station_lons, 'yellow', size=50, marker=True, label=station_names)

gmapOne.draw("map.html")
