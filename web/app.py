from flask import Flask, request, jsonify, render_template
import json
import joblib
import pandas as pd
from datetime import datetime
import os
from web3 import Web3

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

web3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))
contract_address = 'UnitEventRegistry_CONTRACT_ADDRESS'
with open(os.path.join(base_dir, '../blockchain/UnitEventRegistryABI.json'), 'r') as f:
    contract_abi = json.load(f)
contract = web3.eth.contract(address=contract_address, abi=contract_abi)

def parse_timestamp(timestamp):
    for fmt in ('%Y-%m-%dT%H:%M:%S', '%Y-%m-%dT%H:%M'):
        try:
            return datetime.strptime(timestamp, fmt).timestamp()
        except ValueError:
            continue
    raise ValueError(f"time data '{timestamp}' does not match any supported format")

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
    try:
        unix_timestamp = parse_timestamp(timestamp)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    
    input_data = {**options, "timestamp": unix_timestamp}
    input_df = pd.DataFrame([input_data])
    prediction = model.predict(input_df)[0]

    tx_hash = contract.functions.logEvent(
        prediction,
        list(options.values()),
        int(unix_timestamp)
    ).transact({'from': web3.eth.accounts[0]})
    receipt = web3.eth.waitForTransactionReceipt(tx_hash)

    return jsonify({"predicted_event_type": prediction, "transaction_receipt": dict(receipt)})

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
