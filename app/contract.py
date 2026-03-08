import os
from web3 import Web3
from web3.middleware import geth_poa_middleware
from dotenv import load_dotenv

load_dotenv()

# Connect to Ethereum network
w3 = Web3(Web3.HTTPProvider(os.getenv("ETHEREUM_RPC_URL")))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)  # for Sepolia

# Contract ABI (compiled from ContentRegistry.sol)
CONTRACT_ABI = [
    {
        "inputs": [{"internalType": "string", "name": "contentHash", "type": "string"}],
        "name": "register",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [{"internalType": "string", "name": "contentHash", "type": "string"}],
        "name": "verify",
        "outputs": [
            {"internalType": "address", "name": "owner", "type": "address"},
            {"internalType": "uint256", "name": "timestamp", "type": "uint256"},
        ],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": False,
                "internalType": "string",
                "name": "contentHash",
                "type": "string",
            },
            {
                "indexed": False,
                "internalType": "address",
                "name": "owner",
                "type": "address",
            },
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "timestamp",
                "type": "uint256",
            },
        ],
        "name": "ContentRegistered",
        "type": "event",
    },
]

contract_address = os.getenv("CONTRACT_ADDRESS")
private_key = os.getenv("ETHEREUM_PRIVATE_KEY")
account = w3.eth.account.from_key(private_key)

contract = w3.eth.contract(address=contract_address, abi=CONTRACT_ABI)


def register_content_on_chain(content_hash: str) -> dict:
    """Register content hash on blockchain."""
    txn = contract.functions.register(content_hash).build_transaction(
        {
            "from": account.address,
            "nonce": w3.eth.get_transaction_count(account.address),
            "gas": 200000,
            "gasPrice": w3.eth.gas_price,
        }
    )
    signed_txn = w3.eth.account.sign_transaction(txn, private_key)
    tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    return {"tx_hash": tx_hash.hex(), "block_number": receipt["blockNumber"]}


def verify_content_on_chain(content_hash: str) -> dict:
    """Verify content hash on blockchain."""
    try:
        owner, timestamp = contract.functions.verify(content_hash).call()
        return {
            "owner": owner,
            "timestamp": timestamp,
            "exists": owner != "0x0000000000000000000000000000000000000000",
        }
    except Exception as e:
        return {"exists": False, "error": str(e)}
