from flask import Flask, render_template, jsonify
from flask import request
from waitress import serve
# from customPythonFile import customPythonFunction
from flask_cors import CORS
# import json
# import subprocess
from dotenv import load_dotenv
import os
from intake import process_intake
from predict import node_classifier
import json
import logging
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
CORS(app)
# url = "http://localhost:8081/"
# api_key = ""

load_dotenv()

url = "https://compute-server.iaac.net/"; ##//if debugging locally.
api_key = {os.getenv("api_key")}

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process_data():
    # data = intake_data()
    # print(request.data)
    # data = request.get_json(force=True)
    data = json.loads(request.data.decode())
    # print(f"Received data: {data}")
    if not data:
        return jsonify({"error": "Invalid Input"}), 400
    
    # print(f"data type is:"+str(type(data)))
    
    try:
        decoded = process_intake(url, api_key, data)
    except Exception as e:
        logging.error(f"An Error occured during process_intake: {e}")

    # print(f"decoded type is:"+str(type(decoded)))
    # print(decoded[134194:134294])
        
    try:
        decoded_json = json.dumps(decoded)
        with open('assets/decoded.json', 'w', encoding='utf-8') as f:
            json.dump(decoded_json, f, ensure_ascii=False, indent=4)
    except Exception as e:
        logging.error(f"An error occured: {e}")
        return jsonify({"error": "Internal Server error during decode"}), 500
    

    # parsed_data = json.loads(decoded)
    print(f"decoded_json type is:"+str(type(decoded_json)))
    
    try:
        predictions = node_classifier(decoded_json)
    except Exception as e:
        logging.error(f"An error occured: {e}")
        return jsonify({"error": "Internal Server error during predictions"}), 500
 
    # Create a dictionary of node indices and their predicted classes
    prediction_dict = {idx: predicted_class for idx, predicted_class in enumerate(predictions)}
    # print(f"prediction_dict type is:"+str(type(prediction_dict)))
    # Save the dictionary to a JSON file
    # with open('assets/predicted_classes.json', 'w') as json_file:
    #     json.dump(prediction_dict, json_file, indent=4)
    
    # processed_data = execute_json('assets/predicted_classes.json')
        
        # Load nodesAndEdges.json
    # with open('assets/nodesAndEdges.json', 'r') as file:
    #     nodes_and_edges = json.load(file)
        # print(type(nodes_and_edges))
        # Iterate over the nodes in nodesAndEdges and add the predicted class
    corrected_decode_json_string = decoded_json.replace('False', 'false').replace('True', 'true')

    data = json.loads(corrected_decode_json_string)
    if isinstance(data, str):
      dedecoded_json = json.loads(data)
    
    # dedecoded_json = json.loads(decoded_json)
    print(f"dedecoded_json NEW type is:"+str(type(dedecoded_json)))
    
    for node in dedecoded_json['features']:
        # print(f"node in decoded_json['features'] is type:"+str(type(node)))
        # node_id = str(node[0]['properties']['label'])
        # if node_id in processed_data:
        #     node['properties']['predictedClass'] = processed_data[node_id]
        # print(node)
        if 'node' in node and 'properties' in node['node'] and 'label' in node['node']['properties']:
            node_id = node['node']['properties']['label']
            if node_id in prediction_dict:
                node['node']['properties']['predictedClass'] = prediction_dict[node_id]
                print(f"Added predictedClass for node_id: {node_id}")
            else:
                print(f"node_id {node_id} not found in processed_data")
        # Write the combined data back to nodesAndEdges.json (or a new file if you prefer)
    # with open('assets/predictedGraph.json', 'w') as file:
    #     json.dump(nodes_and_edges, file, indent=4)
    predicted_graph = dedecoded_json
    
    # Return processed data as JSON
    # return jsonify(nodes_and_edges)
    return jsonify(predicted_graph)

# def intake_data():
#     # Get JSON data from the request
#     data = request.get_json()
#     # with open("assets/dataObject.json", 'w') as json_file:
#     #     json.dump(data, json_file, indent=4)
#     return data

# def execute_json(filename):
#     with open(filename, "r") as f:
#         return json.load(f)

if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=8000)
