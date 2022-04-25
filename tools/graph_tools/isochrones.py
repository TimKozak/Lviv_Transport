import osmnx as ox
from datetime import datetime
import pandas as pd
import warnings
import networkx as nx
import geopandas as gpd
from shapely.geometry import Point, LineString, Point, Polygon
import geopandas as gpd
import matplotlib.pyplot as plt
from descartes import PolygonPatch
from retrieve_routes import retrieve_routes

warnings.simplefilter(action="ignore", category=FutureWarning)
warnings.simplefilter(action="ignore", category=UserWarning)
warnings.simplefilter(action="ignore", category=PendingDeprecationWarning)
ox.config(use_cache=True, log_console=False)

# Set the location
place = {"city": "Lviv", "country": "Ukraine"}
network_type = "walk"
trip_times = [8]  # in minutes
travel_speed = 4.5  # walking speed in km/hour
Graph = ox.graph_from_place(place, network_type=network_type)
iso_colors = ox.plot.get_colors(n=len(trip_times), cmap="viridis", start=0, return_hex=True)

G = ox.project_graph(Graph)

# Gather isochrones
def make_iso_polys(G, edge_buff=25, node_buff=50, infill=False):
    isochrone_polys = []
    for trip_time in sorted(trip_times, reverse=True):
        subgraph = nx.ego_graph(G, center_node, radius=trip_time, distance="time")

        node_points = [Point((data["x"], data["y"])) for node, data in subgraph.nodes(data=True)]
        nodes_gdf = gpd.GeoDataFrame({"id": list(subgraph.nodes)}, geometry=node_points)
        nodes_gdf = nodes_gdf.set_index("id")

        edge_lines = []
        for n_fr, n_to in subgraph.edges():
            f = nodes_gdf.loc[n_fr].geometry
            t = nodes_gdf.loc[n_to].geometry
            edge_lookup = G.get_edge_data(n_fr, n_to)[0].get("geometry", LineString([f, t]))
            edge_lines.append(edge_lookup)

        n = nodes_gdf.buffer(node_buff).geometry
        e = gpd.GeoSeries(edge_lines).buffer(edge_buff).geometry
        all_gs = list(n) + list(e)
        new_iso = gpd.GeoSeries(all_gs).unary_union

        # try to fill in surrounded areas so shapes will appear solid and
        # blocks without white space inside them
        if infill:
            new_iso = Polygon(new_iso.exterior)
        isochrone_polys.append(new_iso)
    return isochrone_polys


odd_routes, odd_names, even_routes, even_names = retrieve_routes()
odd_coords = [elem for route in odd_routes for elem in route]
even_coords = [elem for route in even_routes for elem in route]

# route = [(49.82202, 23.93662), (49.82219, 23.93651), (49.824, 23.93804), (49.82438, 23.93839), (49.82464, 23.93885), (49.82488, 23.93937), (49.82503, 23.9397), (49.82535, 23.94072), (49.82576, 23.94282), (49.82578, 23.94302), (49.82575, 23.94324), (49.82564, 23.94375), (49.82566, 23.94392), (49.82576, 23.94406), (49.8264, 23.94488), (49.82667, 23.94644), (49.82681, 23.9469), (49.82689, 23.94732), (49.82682, 23.9476), (49.8269, 23.94805), (49.82709, 23.94892), (49.82718, 23.94933), (49.82729, 23.94962), (49.82798, 23.95351), (49.82791, 23.95379), (49.82775, 23.95403), (49.82737, 23.95431), (49.82684, 23.95456), (49.82401, 23.95579), (49.82359, 23.95598), (49.8232, 23.95995), (49.82307, 23.96145), (49.82269, 23.96561), (49.82266, 23.96605), (49.8226, 23.96742), (49.82215, 23.9677), (49.82188, 23.9679), (49.82115, 23.96854), (49.82004, 23.96946), (49.81742, 23.97163), (49.81642, 23.97246), (49.81611, 23.97278), (49.81586, 23.97309), (49.81557, 23.97352), (49.81395, 23.97612), (49.81362, 23.97671), (49.81338, 23.97718), (49.81325, 23.97748), (49.81304, 23.97803), (49.81275, 23.979), (49.81259, 23.9796), (49.81246, 23.98024), (49.81234, 23.98093), (49.8122, 23.98223), (49.81211, 23.98221), (49.8122, 23.98223), (49.81207, 23.98339), (49.81199, 23.98339), (49.81183, 23.98347), (49.81171, 23.98364), (49.81167, 23.98376), (49.81054, 23.98312), (49.80945, 23.98254), (49.80862, 23.98218), (49.80805, 23.98197), (49.80751, 23.9818), (49.80625, 23.98152), (49.80608, 23.98138), 
# (49.8059, 23.98113), (49.80586, 23.98103), (49.80579, 23.98096), (49.80572, 23.98092), (49.80564, 23.9809), (49.80557, 23.98092), (49.8055, 23.98096), (49.80543, 23.98103), (49.80537, 23.98115), (49.80534, 23.98129), (49.80533, 23.98144), (49.80536, 23.98158), (49.80541, 23.9817), (49.80548, 23.98203), (49.80548, 23.98219), (49.80543, 23.98256), (49.80537, 23.98306), (49.80501, 23.98654), (49.80493, 23.98652), (49.80481, 23.98769), (49.80463, 23.98922), (49.80474, 23.98925), (49.8043, 23.99375), (49.80416, 23.99371), (49.80422, 23.99317), (49.80416, 23.99371), (49.8043, 23.99375), (49.80401, 23.99652), (49.80355, 24.00099), (49.80297, 24.00679), (49.80228, 24.01352), (49.80217, 24.0147), (49.80223, 24.01483), (49.80223, 24.01487), (49.80192, 24.01799), (49.80262, 24.01815), (49.80591, 24.01889), (49.80654, 24.01897), (49.80852, 24.01917), (49.81217, 24.01953), (49.8147, 24.01978), (49.81461, 24.02195), (49.81449, 24.02554), (49.81571, 24.02571), (49.81679, 24.0259), (49.81691, 24.02589), (49.81687, 24.02615), (49.81662, 
# 24.02696), (49.8158, 24.02967), (49.81386, 24.03587), (49.81362, 24.03665), (49.81347, 24.03691), (49.81342, 24.03695), (49.8134, 24.03699), (49.81339, 24.03708), (49.81336, 24.03717), (49.81302, 24.03808), (49.81184, 24.04144), (49.81079, 24.0445), (49.81031, 24.04587), (49.81033, 24.04601), (49.81041, 24.04617), (49.81178, 24.04581), (49.8118, 24.04606), (49.8118, 24.04639), (49.81129, 24.05054), (49.81066, 24.05587), (49.81052, 24.05717), (49.81046, 24.05756), (49.81043, 24.0576), (49.81037, 24.05763), (49.8096, 24.05738), (49.8095, 24.05739), (49.80939, 24.05748), (49.80925, 24.0577), (49.80919, 24.05789), (49.80915, 24.05813), (49.80912, 24.05914), (49.80914, 24.06116), (49.81017, 24.06109), (49.81139, 24.06097), (49.81176, 24.06093), (49.8126, 24.06072), (49.81301, 24.06054), (49.81361, 24.06019), (49.81387, 24.06006), (49.81406, 24.06001), (49.81433, 24.06), (49.81454, 24.06001), (49.8147, 24.06005), (49.81493, 24.06018), (49.81509, 24.06032), (49.81518, 24.06044), (49.81589, 24.06147), (49.81595, 24.06172), (49.81597, 24.062), (49.81596, 24.063), (49.816, 24.06446), (49.81604, 24.0654), (49.81619, 24.06788), (49.81617, 24.06828), (49.81607, 24.06909), (49.81593, 24.06989), (49.81579, 24.07048), (49.81532, 24.07229), (49.81451, 24.07536), (49.81421, 24.07648), (49.8141, 24.07697), (49.81404, 24.07737), (49.81398, 24.07781), (49.81396, 24.07818), (49.81398, 24.07835), (49.81702, 24.07718), (49.82255, 24.07507), (49.82281, 24.07498), (49.823, 24.07495), (49.82378, 24.07512), (49.82392, 24.07513), (49.82419, 24.07511), (49.82446, 24.07505), (49.82459, 24.075), (49.82496, 24.07479), (49.82516, 24.07463), (49.82549, 24.07425), (49.8258, 24.07374), (49.8262, 24.07288), (49.82627, 24.07274), (49.82651, 24.07237), (49.82666, 24.07222), (49.82779, 
# 24.07123), (49.83038, 24.06898), (49.83059, 24.06871), (49.8308, 24.06832), (49.83141, 24.06712), (49.83151, 24.06698), (49.83162, 24.06689), (49.83175, 24.06683), (49.83184, 24.06682), (49.83199, 24.06683), (49.83212, 24.06687), (49.83226, 24.06697), (49.83256, 24.06734), (49.83269, 24.06747), 
# (49.83289, 24.06759), (49.83317, 24.06768), (49.83373, 24.0678), (49.83571, 24.06831), (49.83589, 24.06853), (49.836, 24.06876), (49.83592, 24.07091), (49.83592, 24.07106)]

# collect isochrones for each station on the route
isochrones = []
i = 0

for route in odd_routes:
    for coord in route:
        try:
            center_node = center_node = ox.distance.get_nearest_node(Graph, (float(coord[0]), float(coord[1])))
            isochrones.append(make_iso_polys(G, edge_buff=25, node_buff=0, infill=True))
        except:
            pass
    print(f'Isochrones for Route-{i}(odd) collected')
    i += 1

for route in even_routes:
    for coord in route:
        try:
            center_node = center_node = ox.distance.get_nearest_node(Graph, (float(coord[0]), float(coord[1])))
            isochrones.append(make_iso_polys(G, edge_buff=25, node_buff=0, infill=True))
        except:
            pass
    print(f'Isochrones for Route-{i}(even) collected')
    i += 1

# plot map and all the isochrones
fig, ax = ox.plot_graph(
    G, show=False, close=False, edge_color="#999999", edge_alpha=0.2, node_size=0
)

print(f"Number of isochrone_polys: {len(isochrones)}")
i = 0

for isochrone_polys in isochrones:
    for polygon, fc in zip(isochrone_polys, iso_colors):
        patch = PolygonPatch(polygon, fc=fc, ec="none", alpha=0.7, zorder=-1)
        ax.add_patch(patch)
    i += 1

print(f"{i} polygons added!")

fig.savefig(f'./isochrones/{str(datetime.now())[:-7].replace(":", "").replace(" ", "_")}.png', dpi=1200)
plt.show()