let contract;
let account;

async function connectMetaMask() {
    if (window.ethereum) {
        try {
            const accounts = await ethereum.request({ method: 'eth_requestAccounts' });
            account = accounts[0];
            document.getElementById('account').innerText = `Account: ${account}`;
            await loadContract();
        } catch (error) {
            console.error('User denied account access', error);
        }
    } else {
        console.log('MetaMask is not installed');
    }
}

async function loadContract() {
    const contractAddress = 'HumanLifeToken_ADDRESS_HERE';
    const abi = [/* ABI goes here */];
    const web3 = new Web3(window.ethereum);
    contract = new web3.eth.Contract(abi, contractAddress);

    const hasConnected = await contract.methods.hasConnected(account).call();
    if (!hasConnected) {
        await contract.methods.mintFirstTimeToken(account).send({ from: account });
        alert('First time connected to Web3 Life token minted!');
    } else {
        alert('Welcome back! You already have a Web3 Life token.');
    }
}

document.getElementById('connectButton').onclick = connectMetaMask;
