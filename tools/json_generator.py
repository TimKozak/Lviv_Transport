import json
import csv

# READ FILE AND RETURN VALUES ARRAY
def read_file(filename) -> list:
    rows = []

    with open(filename, 'r') as file:
        csvreader = csv.reader(file)
        header = next(csvreader)
        for row in csvreader:
            rows.append(row)

    print(header)

    return rows

# GENERATES UNIQUE COORD VIEW
def generate_coord_view_json(rows) -> str:
    used_addresses = dict()
    stations_dict = dict()

    identifier = 1
    
    for row in rows:
        key = (row[1] + row[2]).lower()

        if key not in used_addresses.keys():
            station = {
                    "routes": [row[0]],
                    "name": row[1],
                    "street": row[2],
                    "coords": (row[3], row[4])
                }

            used_addresses[key] = identifier
            stations_dict[identifier] = station
            identifier += 1
        
        else:
            stations_dict[used_addresses[key]]["routes"].append(row[0])
    
    json_object = json.dumps(stations_dict, ensure_ascii=False)

    with open("stations.json", "w") as outfile:
        outfile.write(json_object)

    return stations_dict


if __name__ == '__main__':
    data = read_file('./data/stations.csv')
    generate_coord_view_json(data)
