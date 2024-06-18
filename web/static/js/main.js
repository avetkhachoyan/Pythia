document.getElementById('loadUnitsButton').addEventListener('click', async () => {
    const response = await fetch('/api/units');
    const units = await response.json();
    document.getElementById('units').innerText = JSON.stringify(units, null, 2);
});

document.getElementById('loadEventsButton').addEventListener('click', async () => {
    const response = await fetch('/api/events');
    const events = await response.json();
    document.getElementById('events').innerText = JSON.stringify(events, null, 2);
});

document.getElementById('predictEventButton').addEventListener('click', async () => {
    const options = {
        option_0: parseFloat(document.getElementById('option_0').value),
        option_1: parseFloat(document.getElementById('option_1').value),
        option_2: parseFloat(document.getElementById('option_2').value),
        option_3: parseFloat(document.getElementById('option_3').value),
        option_4: parseFloat(document.getElementById('option_4').value),
    };
    const timestamp = document.getElementById('timestamp').value;

    const response = await fetch('/api/predict', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ options, timestamp }),
    });

    const result = await response.json();
    document.getElementById('prediction').innerText = JSON.stringify(result, null, 2);
});
