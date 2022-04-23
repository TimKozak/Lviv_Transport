import json
import csv

def read_file(filename) -> list:
    rows = []

    with open(filename, "r") as file:
        csvreader = csv.reader(file)
        header = next(csvreader)
        for row in csvreader:
            rows.append(row)

    return rows

def convert_shapes_to_json(shapes):
    shapes_dict = {}

    for shape in shapes:
        if shape[0] not in shapes_dict:
            shapes_dict[shape[0]] = [[float(shape[1]), float(shape[2]), float(shape[4])]]
        else:
            shapes_dict[shape[0]].append([float(shape[1]), float(shape[2]), float(shape[4])])

    json_object = json.dumps(shapes_dict, ensure_ascii=False)

    with open("shapes.json", "w") as outfile:
        outfile.write(json_object)

    return shapes_dict


if __name__ == "__main__":
    shapes = read_file("./data/shape.csv")
    convert_shapes_to_json(shapes)