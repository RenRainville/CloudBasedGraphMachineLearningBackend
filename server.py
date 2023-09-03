from flask import Flask, request, render_template, jsonify
from waitress import serve
# from customPythonFile import customPythonFunction
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])

def intakeData():
    # Get JSON data from the request
    data = request.get_json()
    with open("assets/dataObject.json", 'w') as json_file:
        json.dump(data, json_file, indent=4)
    return data

def execute(filename):
    f = open(filename, "r")
    r = (f.read())
    f.close()
    return r

def process_data():
    # exec(open('intake.py').read())
    # execute intake.py to process web output to graph form
    execute('intake.py')
    # Do some processing here...
    execute('predict.py')
    
    processed_data = execute('output.json') # Just echo the data back

    # Return processed data as JSON
    return jsonify(processed_data)

if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=8000)
