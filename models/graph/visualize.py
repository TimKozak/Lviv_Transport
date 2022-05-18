import gmplot

import construct_graph


def visualize_distant_stops():

    df = construct_graph.graph_creation()
    df = df[df["route_changes"] >= 4]
    print(df)
    # print(df)
    gmapOne = gmplot.GoogleMapPlotter(49.8, 23.9, 15)

    lats = df["lat"].to_list()
    lons = df["lon"].to_list()
    stations = df["station"].to_list()

    gmapOne.scatter(
        lats, lons, "#ff0000", alpha=1, size=40, marker=True, symbol="o", label=stations
    )

    gmapOne.draw("distant_stations.html")


if __name__ == "__main__":
    visualize_distant_stops()
