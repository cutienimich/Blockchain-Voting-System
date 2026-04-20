from web3 import Web3
from dotenv import load_dotenv
import json
import os

load_dotenv()

RPC_URL = os.getenv("BLOCKCHAIN_RPC_URL")
CONTRACT_ADDRESS = os.getenv("CONTRACT_ADDRESS")
PRIVATE_KEY = os.getenv("DEPLOYER_PRIVATE_KEY")

# ─── CONNECT ─────────────────────────────────────
w3 = Web3(Web3.HTTPProvider(RPC_URL))

# ─── ABI ─────────────────────────────────────────
ABI = [
    {
        "inputs": [
            {"internalType": "uint256", "name": "_userId", "type": "uint256"},
            {"internalType": "uint256", "name": "_electionId", "type": "uint256"},
            {"internalType": "uint256", "name": "_candidateId", "type": "uint256"}
        ],
        "name": "castVote",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {"internalType": "uint256", "name": "_electionId", "type": "uint256"},
            {"internalType": "uint256", "name": "_candidateId", "type": "uint256"}
        ],
        "name": "getVoteCount",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {"internalType": "uint256", "name": "_electionId", "type": "uint256"},
            {"internalType": "uint256", "name": "_userId", "type": "uint256"}
        ],
        "name": "checkVoted",
        "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
        "stateMutability": "view",
        "type": "function"
    }
]

# ─── CONTRACT INSTANCE ───────────────────────────
contract = w3.eth.contract(
    address=Web3.to_checksum_address(CONTRACT_ADDRESS),
    abi=ABI
)

# ─── SEND VOTE TO BLOCKCHAIN ─────────────────────
def send_vote_to_blockchain(user_id: int, election_id: int, candidate_id: int):
    try:
        account = w3.eth.account.from_key(PRIVATE_KEY)
        
        tx = contract.functions.castVote(
            user_id,
            election_id,
            candidate_id
        ).build_transaction({
            "from": account.address,
            "nonce": w3.eth.get_transaction_count(account.address),
            "gas": 200000,
            "gasPrice": w3.eth.gas_price
        })

        signed_tx = w3.eth.account.sign_transaction(tx, PRIVATE_KEY)
        tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
        receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

        return receipt.transactionHash.hex()

    except Exception as e:
        print(f"Blockchain error: {e}")
        return None