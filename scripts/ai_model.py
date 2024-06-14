import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import json
import joblib
from datetime import datetime

with open('data/units.json', 'r') as f:
    units = json.load(f)

with open('data/events.json', 'r') as f:
    events = json.load(f)

data = []

for event in events:
    for unit_id in event['unit_ids']:
        unit = next(unit for unit in units if unit['id'] == unit_id)
        row = {**unit['options'], "event_type": event['event_type'], "timestamp": event['timestamp']}
        data.append(row)

df = pd.DataFrame(data)

df['timestamp'] = df['timestamp'].apply(lambda x: datetime.fromisoformat(x).timestamp())

X = df.drop(columns=["event_type"])
y = df["event_type"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

predictions = model.predict(X_test)

accuracy = model.score(X_test, y_test)
print(f"Model Accuracy: {accuracy * 100:.2f}%")

joblib.dump(model, 'models/event_prediction_model.joblib')
