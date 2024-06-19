// static/js/main.js

document.addEventListener("DOMContentLoaded", function() {
    if (typeof window.ethereum !== 'undefined') {
        ethereum.request({ method: 'eth_requestAccounts' })
            .then(accounts => {
                const account = accounts[0];
                document.getElementById('account').innerText = `Account: ${account}`;

                ethereum.request({ method: 'eth_getBalance', params: [account, 'latest'] })
                    .then(balance => {
                        document.getElementById('balance').innerText = `Balance: ${Web3.utils.fromWei(balance, 'ether')} ETH`;
                    });

                // Fetch transactions and update the model
                fetch('/api/update_model')
                    .then(response => response.json())
                    .then(data => {
                        console.log('Model updated:', data.message);
                    })
                    .catch(error => console.error('Error updating model:', error));
            })
            .catch(error => console.error('Error connecting to MetaMask:', error));
    } else {
        console.log('MetaMask is not installed');
    }
});

async function fetchUnits() {
    const response = await fetch('/api/units');
    const units = await response.json();
    document.getElementById('units').innerText = JSON.stringify(units, null, 2);
}

async function fetchEvents() {
    const response = await fetch('/api/events');
    const events = await response.json();
    document.getElementById('events').innerText = JSON.stringify(events, null, 2);
}

async function predictEvent() {
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
}
