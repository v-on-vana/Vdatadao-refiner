from web3 import Web3
import os

# Configuration for Vana Mainnet
RPC_URL = os.getenv("NEXT_PUBLIC_NETWORK_RPC_URL", "https://rpc.vana.org")
DLP_CONTRACT_ADDRESS = os.getenv("NEXT_PUBLIC_DLP_CONTRACT_ADDRESS", "0xdD29F495C058C7f13A7eb07428De3a46462E1909")

# ABI for publicKey function
DLP_CONTRACT_ABI = [
    {
        "inputs": [],
        "name": "publicKey",
        "outputs": [{"internalType": "string", "name": "", "type": "string"}],
        "stateMutability": "view",
        "type": "function"
    }
]

class BlockchainReader:
    def __init__(self):
        self.w3 = Web3(Web3.HTTPProvider(RPC_URL))
        self.dlp_contract = self.w3.eth.contract(
            address=Web3.to_checksum_address(DLP_CONTRACT_ADDRESS),
            abi=DLP_CONTRACT_ABI
        )

    def get_encryption_key(self) -> str:
        try:
            # Read the public key using publicKey function
            encryption_key = self.dlp_contract.functions.publicKey().call()
            if encryption_key:
                print(f"✅ Encryption key retrieved from DLP contract: {encryption_key}")
                return encryption_key
            else:
                print(f"⚠️  Encryption key not found in DLP contract")
                return ""
        except Exception as e:
            print(f"❌ Error retrieving encryption key from DLP contract: {e}")
            return ""

blockchain_reader = BlockchainReader()
