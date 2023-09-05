from flask import Flask, request, render_template, jsonify
from waitress import serve
# from customPythonFile import customPythonFunction
from flask_cors import CORS
import json
import subprocess
from intake import process_intake
from predict import node_classifier

app = Flask(__name__)
CORS(app)
url = "http://localhost:8081/"
api_key = ""

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process_data():
    intake_data()
    process_intake(url, api_key)
    predictions = node_classifier()
    
    # Create a dictionary of node indices and their predicted classes
    prediction_dict = {idx: predicted_class for idx, predicted_class in enumerate(predictions)}
    
    # Save the dictionary to a JSON file
    with open('assets/predicted_classes.json', 'w') as json_file:
        json.dump(prediction_dict, json_file, indent=4)
    
    processed_data = execute_json('predicted_classes.json')
    
    # Load nodesAndEdges.json
    with open('nodesAndEdges.json', 'r') as file:
        nodes_and_edges = json.load(file)
    
    # Iterate over the nodes in nodesAndEdges and add the predicted class
    for node in nodes_and_edges:
        node_id = str(node['properties']['label'])  # Convert to string to match predicted_classes keys
        if node_id in processed_data:
            node['properties']['predictedClass'] = processed_data[node_id]
    
    # Write the combined data back to nodesAndEdges.json (or a new file if you prefer)
    with open('predicatedGraph.json', 'w') as file:
        json.dump(nodes_and_edges, file, indent=4)
    
    # Return processed data as JSON
    return jsonify(nodes_and_edges)

def intake_data():
    # Get JSON data from the request
    data = request.get_json()
    with open("assets/dataObject.json", 'w') as json_file:
        json.dump(data, json_file, indent=4)
    return data

def execute_json(filename):
    with open(filename, "r") as f:
        return json.load(f)

if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=8000)
