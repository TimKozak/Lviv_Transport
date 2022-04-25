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

def gen_layer(route):
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

    # collect isochrones for each station on the route
    isochrones = []

    for coord in route:
        try:
            center_node = center_node = ox.distance.get_nearest_node(Graph, (float(coord[0]), float(coord[1])))
            isochrones.append(make_iso_polys(G, edge_buff=25, node_buff=0, infill=True))
        except:
            pass
    print(f'Isochrones for Route collected')

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


if __name__ == '__main__':

    # Set the location
    place = {"city": "Lviv", "country": "Ukraine"}
    network_type = "walk"
    trip_times = [8]  # in minutes
    travel_speed = 4.5  # walking speed in km/hour
    Graph = ox.graph_from_place(place, network_type=network_type)
    iso_colors = ox.plot.get_colors(n=len(trip_times), cmap="viridis", start=0, return_hex=True)

    G = ox.project_graph(Graph)

    odd_routes, odd_names, even_routes, even_names = retrieve_routes()

    for route in odd_routes:
        gen_layer(route)
    
    for route in even_routes:
        gen_layer(route)