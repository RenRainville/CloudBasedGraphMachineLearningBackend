from flask import Flask, request, render_template, jsonify
from waitress import serve
# from customPythonFile import customPythonFunction
from flask_cors import CORS
import json
import subprocess
from intake import process_intake

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
    result = process_intake(url, api_key)
    # exec(open('intake.py').read())
    # execute intake.py to process web output to graph form
    # execute('intake.py')
    # Do some processing here...
    execute('predict.py')
    
    processed_data = execute_json('predicted_classes.json') # Just echo the data back

    # Return processed data as JSON
    return jsonify(processed_data)

def intake_data():
    # Get JSON data from the request
    data = request.get_json()
    with open("assets/dataObject.json", 'w') as json_file:
        json.dump(data, json_file, indent=4)
    return data

def execute(filename):
    with open(filename, 'r') as file:
        code = file.read()
        exec(code)

def execute_json(filename):
    with open(filename, "r") as f:
        return json.load(f)

if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=8000)
