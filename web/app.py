from flask import Flask, request, jsonify, render_template
import json
import joblib
import pandas as pd
from datetime import datetime
import os

app = Flask(__name__, static_url_path='', static_folder='static', template_folder='templates')

base_dir = os.path.abspath(os.path.dirname(__file__))
units_path = os.path.join(base_dir, '../data/units.json')
events_path = os.path.join(base_dir, '../data/events.json')
model_path = os.path.join(base_dir, '../models/event_prediction_model.joblib')

with open(units_path, 'r') as f:
    units = json.load(f)

with open(events_path, 'r') as f:
    events = json.load(f)

model = joblib.load(model_path)

@app.route('/api/units', methods=['GET'])
def get_units():
    return jsonify(units)

@app.route('/api/events', methods=['GET'])
def get_events():
    return jsonify(events)

@app.route('/api/predict', methods=['POST'])
def predict_event():
    data = request.json
    options = data['options']
    timestamp = data['timestamp']
    input_data = {**options, "timestamp": datetime.timestamp(datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S"))}
    input_df = pd.DataFrame([input_data])
    prediction = model.predict(input_df)[0]
    return jsonify({"predicted_event_type": prediction})

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
