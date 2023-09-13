import json
# import requests
import matplotlib.pyplot as plt
from shapely.geometry import Polygon
import compute_rhino3d.Util
import compute_rhino3d.Grasshopper as gh

def process_intake(url, api_key, data, defName='assets/FloorPlanGenerator_Combined.gh'):
    compute_rhino3d.Util.url = url
    compute_rhino3d.Util.apiKey = api_key

    # defName = 'assets/FloorPlanGenerator_Combined.gh'

    # file_path = 'assets/dataObject.json'

    # try:
    #     with open(file_path, 'r') as file:
    #         data = json.load(file)
    # except FileNotFoundError:
    #     print(f'The file {file_path} was not found.')

    # except json.JSONDecodeError:
    #     print(f'Error decoding JSON from {file_path}.')


    try:
        if 'geometry' in data and 'type' in data['geometry']:
            
            lineType = data['geometry']['type']
            # print(lineType)
            lineType_tree = gh.DataTree('RH_IN:lineType')
            lineType_tree.Append([0], [lineType])
            # lineType = lineType_tree
        else:
            print(f'expected keys not found in data')
            
        vertices = data['geometry']['coordinates'][0:]
        # print(vertices)
        vertices_tree = gh.DataTree('RH_IN:vertices')
        for v in range(len(vertices)):
            vertices_tree.Append([0], [v])
        # vertices = vertices_tree

        corrType = data['properties']['corridorType']
        Dict = {"double loaded": 0, "single loaded": 1}
        corridor = Dict[corrType]
        # print(corridor)
        corr_tree = gh.DataTree('RH_IN:corridor')
        corr_tree.Append([0], [corridor])
        # corridor = corr_tree

        levels = data['properties']['floorsInput']
        # print(levels)
        levels_tree = gh.DataTree('RH_IN:levels')
        levels_tree.Append([0], [levels])
        # levels = levels_tree
    except Exception as e:
        print(f'Error constructing DataTree: {e}.')

    trees = [lineType_tree, vertices_tree, corr_tree, levels_tree]
    # trees = [lineType, vertices, corrType, levels]

    # trees_data = [tree.data for tree in trees]
    #print(trees_data)

    nodesAndEdges = str()
    output = {}
    decoded_data = {}

    try:
        output = gh.EvaluateDefinition(defName, trees)
        # decoding output
        branch = output['values'][0]['InnerTree']['{0}'][0]
        nodesAndEdges = branch['data']
        # print(nodesAndEdges)
        # print(f"nodesAndeEdges type is:"+type(nodesAndEdges))
        decoded_data = json.loads(nodesAndEdges)
        # print(f"decoded_data type is:"+type(decoded_data))
        # print(type(decoded_data))

    except Exception as e:
        print(f'Error running grasshopper file: {e}.')


    if output:
    
        # print("Writing to JSON file with data: ", decoded_data)
        # # writing JSON data
        # with open("assets/nodesAndEdges.json", 'w') as f:
        #     # json.dump(string_data, f)
        #     # json.dump(swapped_data, f)
        #     # f.write(nodesAndEdges)  
        #     f.write(decoded_data)   
        return decoded_data   
    return None

# url = "https://compute-server.iaac.net/"; ##//if debugging locally.
# api_key = "Pujades102"

# file_path = 'assets/dataObject.json'

# try:
#     with open(file_path, 'r') as file:
#         data = json.load(file)
# except FileNotFoundError:
#     print(f'The file {file_path} was not found.')

# except json.JSONDecodeError:
#     print(f'Error decoding JSON from {file_path}.')

# process_data = process_intake(url,api_key,data)
# print(process_data)