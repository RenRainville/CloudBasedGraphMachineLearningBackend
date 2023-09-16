import json
# import requests
import matplotlib.pyplot as plt
from shapely.geometry import Polygon
import compute_rhino3d.Util
import compute_rhino3d.Grasshopper as gh

def process_intake(url, api_key, data, defName='assets/FloorPlanGenerator_Combined.gh'):
    compute_rhino3d.Util.url = url
    compute_rhino3d.Util.apiKey = api_key

    try:
        if 'geometry' in data and 'type' in data['geometry']:
            
            lineType = data['geometry']['type']
            print(lineType)
            lineType_tree = gh.DataTree('RH_IN:lineType')
            lineType_tree.Append([0], [lineType])
            # lineType = lineType_tree
        else:
            print(f'expected keys not found in data')
            


        vertices = data['geometry']['coordinates']
        x_coordinates = [coord[0] for coord in vertices]
        y_coordinates = [coord[1] for coord in vertices]

        # Create comma-separated strings for X and Y coordinates
        x_string = ', '.join(map(str, x_coordinates))
        y_string = ', '.join(map(str, y_coordinates))

        # Update the x_tree and y_tree data trees
        x_tree = gh.DataTree('RH_IN:x')
        y_tree = gh.DataTree('RH_IN:y')

        for i, (x, y) in enumerate(zip(x_coordinates, y_coordinates)):
            x_tree.Append([0, i], [x])
            y_tree.Append([0, i], [y])

        # Print the combined X and Y coordinates as a single text string
        combined_coordinates = f'X coordinates: {x_string}\nY coordinates: {y_string}'
        print(combined_coordinates)


        corrType = data['properties']['corridorType']
        Dict = {"double loaded": 1, "single loaded": 0}
        corridor = Dict[corrType]
        print(corridor)
        corr_tree = gh.DataTree('RH_IN:corridor')
        corr_tree.Append([0], [corridor])
        # corridor = corr_tree

        levels = data['properties']['floorsInput']
        print(levels)
        levels_tree = gh.DataTree('RH_IN:levels')
        levels_tree.Append([0], [levels])
        # levels = levels_tree
    except Exception as e:
        print(f'Error constructing DataTree: {e}.')

    trees = [lineType_tree, x_tree, y_tree, corr_tree, levels_tree]

    nodesAndEdges = str()
    output = {}
    decoded_data = {}

    try:
        output = gh.EvaluateDefinition(defName, trees)
        # decoding output
        print(output)
        # print(nodesAndEdges)
        # print(f"nodesAndeEdges type is:"+type(nodesAndEdges))
        # print(f"decoded_data type is:"+type(decoded_data))
        # print(type(decoded_data))

    except Exception as e:
        print(f'Error running grasshopper file: {e}.')

    try:

        branch = output['values'][0]['InnerTree']['{0}'][0]
        nodesAndEdges = branch['data']

    except Exception as e:
        print(f'Error branch: {e}.')

    try:

        decoded_data = json.loads(nodesAndEdges)


    except Exception as e:
        print(f'Error decoded_data: {e}.')


    if output:
     
        return decoded_data   
    return None