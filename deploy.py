from dis import Bytecode
from solcx import compile_standard
import json
from web3 import Web3
import os
from dotenv import load_dotenv

load_dotenv()
with open("./SimpleStorage.sol", "r") as file:
    simple_storage_file = file.read()
    print(simple_storage_file)
# Compile our solidity

compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleStorage.sol": {"content": simple_storage_file}},
        "settings": {
            "outputSelection": {
                "*": {"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}
            }
        },
    },
    solc_version="0.6.0",
)

with open("compiled_code.json", "w") as file:
    json.dump(compiled_sol, file)
print(compiled_sol)


# Get Bytecode

bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"][
    "bytecode"
]["object"]

# Get ABI[Application Binary Interface]

abi = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["abi"]

# For connecting to ganache
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))
chain_id = 1337
my_address = "0x2F30d56D1509d960D7E183772cf761B9877A7d27"
private_key = os.getenv("PRIVATE_KEY")
print(private_key)

# Create the contract in python
SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)
print(SimpleStorage)

# Get the latestest transaction
nonce = w3.eth.getTransactionCount(my_address)
print(nonce)

# Build a transaction
# sign a transaction
# send a transaction

transaction = SimpleStorage.constructor().buildTransaction( {
    "gasPrice": w3.eth.gas_price, 
    "chainId": chain_id, 
    "from": my_address, 
    "nonce": nonce, 
}

)

# transaction = SimpleStorage.constructor().buildTransaction(
#    {"chainId": chain_id, "from": my_address, "nonce": nonce}
# )
print(transaction)

signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)
print(signed_txn)


# send the signed transaction
tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

# working with the contract
# contract address
# contract ABI
simple_storage = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)
# call -> Simulate making the call and getting a return value
# Transaction -> Actually make a state change

# Initial value of favorite number
print(simple_storage.functions.retrieve().call())
store_trasaction = simple_storage.functions.store(15).buildTransaction(
    {"chainID": chain_id, "from": my_address, "nonce": nonce + 1}
)

signed_store_txn = w3.eth.account.sign_transaction(
    store_trasaction, private_key=private_key
)
send_store_tx = w3.eth.send_raw_transaction(signed_store_txn.rowTransaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(send_store_tx)
print("Updated!!")
# print(simple_storage.functions.store(15).call())
print(simple_storage.functions.retrieve().call())
