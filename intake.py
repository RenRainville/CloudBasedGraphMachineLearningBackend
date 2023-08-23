import json
import matplotlib.pyplot as plt
from shapely.geometry import Polygon
import compute_rhino3d.Util
import compute_rhino3d.Grasshopper as gh


compute_rhino3d.Util.url = "http://localhost:8081/"
#compute_rhino3d.Util.apiKey = ""

defName = 'assets/FloorPlanGenerator_Combined.gh'

file_path = 'assets/DataFromJS.json'

try:
    with open(file_path, 'r') as file:
        data = json.load(file)
except FileNotFoundError:
    print(f'The file {file_path} was not found.')

except json.JSONDecodeError:
    print(f'Error decoding JSON from {file_path}.')


try:
    lineType = data['geometry']['type']
    lineType_tree = gh.DataTree('RH_IN:lineType')
    lineType_tree.Append([0], [lineType])
    # lineType = lineType_tree

    vertices = data['geometry']['coordinates'][0]
    vertices_tree = gh.DataTree('RH_IN:vertices')
    vertices_tree.Append([0], [vertices])
    # vertices = vertices_tree

    corrType = data['properties']['corridorType']
    Dict = {"double loaded": 0, "single loaded": 1}
    corridor = Dict[corrType]
    corr_tree = gh.DataTree('RH_IN:corridor')
    corr_tree.Append([0], [corridor])
    # corridor = corr_tree

    levels = data['properties']['floorsInput']
    levels_tree = gh.DataTree('RH_IN:levels')
    levels_tree.Append([0], [levels])
    # levels = levels_tree
except Exception as e:
    print(f'Error constructing DataTree: {e}.')

trees = [lineType_tree, vertices_tree, corr_tree, levels_tree]

trees_data = [tree.data for tree in trees]
print(trees_data)

# output = gh.EvaluateDefinition(defName, trees)
# print(output)

# Convert the dictionary to a JSON string
# json_string = json.dumps(output, indent=4)
json_string = json.dumps(output)

# Write the JSON string to a file
with open("assets/output.json", "w") as json_file:
    json_file.write(json_string)