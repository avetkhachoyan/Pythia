# web/app.py

import json
import os
from flask import Flask, request, jsonify
from web3 import Web3
from sklearn.externals import joblib
import pandas as pd
from datetime import datetime

app = Flask(__name__)
w3 = Web3(Web3.HTTPProvider('http://localhost:8545'))

# Load contract ABI and address
with open('../static/HumanLifeTokenABI.json', 'r') as abi_file:
    contract_abi = json.load(abi_file)

contract_address = 'HumanLifeToken_CONTRACT_ADDRESS'
contract = w3.eth.contract(address=contract_address, abi=contract_abi)

# Load the prediction model
model = joblib.load('../models/event_prediction_model.joblib')

# Define a route to fetch accounts and transactions
@app.route('/api/update_model', methods=['GET'])
def update_model():
    accounts = w3.eth.accounts
    transactions = []

    # Iterate over accounts to fetch transactions
    for account in accounts:
        balance = w3.eth.get_balance(account)
        tx_count = w3.eth.get_transaction_count(account)
        transactions.append({
            'account': account,
            'balance': balance,
            'tx_count': tx_count
        })

    # Update the model based on new transactions
    df = pd.DataFrame(transactions)
    features = df[['balance', 'tx_count']]
    labels = df['tx_count']  # This is a placeholder, replace with actual labels

    # Fit the model with new data
    model.fit(features, labels)
    joblib.dump(model, '../models/event_prediction_model.joblib')

    return jsonify({'message': 'Model updated successfully'})


@app.route('/api/predict', methods=['POST'])
def predict_event():
    data = request.json
    options = data['options']
    timestamp = data['timestamp']
    input_data = {**options, "timestamp": datetime.timestamp(datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S"))}

    prediction = model.predict([list(input_data.values())])
    return jsonify({'prediction': prediction.tolist()})


if __name__ == '__main__':
    app.run(debug=True)
