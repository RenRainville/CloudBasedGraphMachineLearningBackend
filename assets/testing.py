import json
    
def execute_json(filename):
    with open(filename, "r") as f:
        return json.load(f)

processed_data = execute_json('assets/predicted_classes.json')
    
    # Load nodesAndEdges.json
with open('assets/nodesAndEdges.json', 'r') as file:
    nodes_and_edges = json.load(file)
    # print(type(nodes_and_edges))
    # Iterate over the nodes in nodesAndEdges and add the predicted class
for node in nodes_and_edges['features'][0]:
    # print(type(node))
    # node_id = str(node[0]['properties']['label'])
    # if node_id in processed_data:
    #     node['properties']['predictedClass'] = processed_data[node_id]
    # print(node)
    if 'node' in node and 'properties' in node['node'] and 'label' in node['node']['properties']:
        node_id = str(node['node']['properties']['label'])
        if node_id in processed_data:
            node['node']['properties']['predictedClass'] = processed_data[node_id]
            print(f"Added predictedClass for node_id: {node_id}")
        else:
            print(f"node_id {node_id} not found in processed_data")
    # Write the combined data back to nodesAndEdges.json (or a new file if you prefer)
with open('assets/predictedGraph.json', 'w') as file:
    json.dump(nodes_and_edges, file, indent=4)