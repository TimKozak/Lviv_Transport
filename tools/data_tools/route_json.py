import pandas as pd
import json

def find_stops(dct, df):
    lines_dct = dict()
    for shape_id in dct:
        lines_dct[shape_id] = []
        for x_coor, y_coor, dist in dct[shape_id]:
            coords = find_within_10m(x_coor, y_coor, df)
            if coords not in lines_dct[shape_id]:
                coords[2] = dist
                lines_dct[shape_id].append(coords)
            else:
                pass
    return lines_dct


def find_within_10m(x, y, df):
    df1 = df[(abs(df['stop_lat'] - x) <= 0.00015) & (abs(df['stop_lon'] - y) <= 0.00015)]
    # df2 = df1[abs(df['stop_lon'] - y) <= 0.0001]
    if df1.size > 0:
        stop_name = (df1["stop_name"].iloc[0])
        return [x, y, None, stop_name]
    else:
        return [x, y, None, None]



def get_df_lst(filename="stop3.csv"):
    df = pd.read_csv(filename)
    # coords = df[['stop_lat', 'stop_lon']].apply(tuple, axis=1).tolist()
    # lon = df['stop_lon'].tolist()
    return df

if __name__=="__main__":
    df = get_df_lst()
    with open("shapes.json", encoding='utf-8') as f:
        dct = json.load(f)
    # print(dct)

    lines_dct = find_stops(dct, df)
    # # lines_dct = find_within_10m(49.83592, 24.07106, df)
    with open("shapes_routes.json", "w", encoding='utf-8') as f:
        json.dump(lines_dct, f, ensure_ascii=False, indent = 4) 