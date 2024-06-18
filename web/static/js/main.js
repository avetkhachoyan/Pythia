async function connectMetaMask() {
    if (window.ethereum) {
        try {
            const accounts = await ethereum.request({ method: 'eth_requestAccounts' });
            const account = accounts[0];
            document.getElementById('account').innerText = `Account: ${account}`;

            const balance = await ethereum.request({
                method: 'eth_getBalance',
                params: [account, 'latest']
            });
            const etherBalance = parseFloat(ethers.utils.formatEther(balance)).toFixed(4);
            document.getElementById('balance').innerText = `Balance: ${etherBalance} ETH`;
        } catch (error) {
            console.error('User denied account access', error);
        }
    } else {
        console.log('MetaMask is not installed');
    }
}

document.getElementById('connectButton').onclick = connectMetaMask;
