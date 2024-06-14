import random
import uuid
from datetime import datetime, timedelta
import json

class Unit:
    def __init__(self, options):
        self.id = str(uuid.uuid4())
        self.options = options

class Event:
    def __init__(self, event_type, unit_ids, timestamp):
        self.id = str(uuid.uuid4())
        self.event_type = event_type
        self.unit_ids = unit_ids
        self.timestamp = timestamp.isoformat()

def generate_units(num_units):
    units = []
    for _ in range(num_units):
        options = {f"option_{i}": random.random() for i in range(5)}
        unit = Unit(options)
        units.append(unit)
    return units

def generate_events(units, num_events):
    event_types = ["birth", "meeting", "interaction_positive", "interaction_negative", "interaction_neutral", "separation", "death"]
    events = []
    for _ in range(num_events):
        event_type = random.choice(event_types)
        unit_ids = random.sample([unit.id for unit in units], k=random.randint(1, 3))
        timestamp = datetime.now() + timedelta(days=random.randint(0, 365))
        event = Event(event_type, unit_ids, timestamp)
        events.append(event)
    return events

units = generate_units(10)
events = generate_events(units, 20)

with open('data/units.json', 'w') as f:
    json.dump([unit.__dict__ for unit in units], f, indent=4)

with open('data/events.json', 'w') as f:
    json.dump([event.__dict__ for event in events], f, indent=4)
