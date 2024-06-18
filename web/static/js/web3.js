document.getElementById('connectButton').addEventListener('click', async () => {
    if (typeof window.ethereum !== 'undefined') {
        try {
            const accounts = await window.ethereum.request({ method: 'eth_requestAccounts' });
            const account = accounts[0];
            document.getElementById('accountInfo').innerText = `Connected account: ${account}`;

            const abi = await fetch('./blockchain/contracts/HumanLifeTokenABI.json').then(response => response.json());
            const contractAddress = 'HumanLifeToken_CONTRACT_ADDRESS_HERE';
            const web3 = new Web3(window.ethereum);
            const contract = new web3.eth.Contract(abi, contractAddress);

            const hasConnected = await contract.methods.hasConnected(account).call();
            if (!hasConnected) {
                await contract.methods.mintFirstTimeToken(account).send({ from: account });
                alert('First time connected to Web3 Life token minted!');
            } else {
                alert('Welcome back! You already have a Web3 Life token.');
            }
        } catch (error) {
            console.error('Error connecting to MetaMask', error);
        }
    } else {
        alert('Please install MetaMask!');
    }
});
