from flask import Flask, request, jsonify
import json
import joblib
import pandas as pd
from datetime import datetime

app = Flask(__name__)

with open('../data/units.json', 'r') as f:
    units = json.load(f)

with open('../data/events.json', 'r') as f:
    events = json.load(f)

model = joblib.load('../models/event_prediction_model.joblib')

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

if __name__ == '__main__':
    app.run(debug=True)
