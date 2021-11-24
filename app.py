from web3 import Web3, middleware
from web3.exceptions import ContractLogicError
from web3.middleware import geth_poa_middleware
from web3.gas_strategies.time_based import *
import os
import json
from dotenv import load_dotenv
import pandas as pd
import streamlit as st

# build streamlit interface
side_click = st.sidebar.write("Contributors: John P Weldon, Ashley Guidot, Forrest Surles, Vishwanath Subramanian")

st.image('https://image.cnbcfm.com/api/v1/image/106962967-1634709558798-gettyimages-1235570383-porzycki-cryptocu210928_npbUe.jpeg?v=1635185551', width=350)

st.markdown("### Smart Risk Movements")
st.markdown("This application assists client portfolio management by calculating transaction fees associated with transferring between Ethereum and a fund before enabling the client to initiate the transfer. The application then automates the transfer of the amount between Etherum and a fund.")

# Load .env environment variables
PRJ3_folder = os.path.expanduser('~/Dropbox/FinTech-Workspace/project_03')  # adjust yours as appropriate
load_dotenv((os.path.join(PRJ3_folder, 'prjenv.env')))
PRIVATE_KEY_ONE = os.getenv("PRIVATE_KEY_1")

# Copy bytecode from Remix to utilize smart contract locally
bytecode = json.load(open('bytecode.json'))['object']
# Copy abi from Remix
abi = json.load(open('abi.json'))


# query input from user to initiate transaction

# wallet address
address_one= st.text_input("Enter your Market Account Address:")
st.write(address_one)

# private key
priv_key_input = st.text_input("Enter your Private Key:", type="password")

# options for transaction
options = st.selectbox("Which account would you like to transfer from?",
        ["Market Account", "Eth Account"])

# give notice of transaction fees
st.markdown("The fee associated with this transaction is 21,000 GWEI.")

# clarify intent from user
fee_agreement = st.selectbox("Would you like to proceed with transaction?",
        ["Yes", "No"])


# execute transaction with user input

# connect to blockchain network
ganache_url = "http://127.0.0.1:7545"
w3 = Web3(Web3.HTTPProvider(ganache_url))

# web3 function that allows us to set the amount of time we want transactions to take (in secs)
strategy = construct_time_based_gas_price_strategy(15)
# Sets the gas price
w3.eth.setGasPriceStrategy(strategy)

our_contract = w3.eth.contract(abi=abi, bytecode=bytecode)


# provide firm wallet address to receive transaction fee
address_two = '0x2CAf7eC7Fe79599C0F2a68b566B52F97D13ff7dD'

# address two private key
PRIVATE_KEY_TWO = os.getenv("PRIVATE_KEY_2")

if fee_agreement == 'Yes' and st.button('Execute'):

        # Getting nonce
        # Using toHex for easier visability when deployed
        gasPrice = 21000 #gwei

        if options == "Market Account":

                nonce = Web3.toHex(w3.eth.getTransactionCount(address_one))

                tr = {'to': address_two, 
                        'from': address_one,
                        'value': Web3.toHex(0), 
                        'gasPrice': Web3.toHex(gasPrice), 
                        'nonce': nonce,
                        'data': "0x" + bytecode,
                        'gas': 5000000,
                        }
                signed = w3.eth.account.sign_transaction(tr, priv_key_input)
        else:

                nonce = Web3.toHex(w3.eth.getTransactionCount(address_two))

                tr = {'to': address_one, 
                        'from': address_two,
                        'value': Web3.toHex(0), 
                        'gasPrice': Web3.toHex(gasPrice), 
                        'nonce': nonce,
                        'data': "0x" + bytecode,
                        'gas': 5000000,
                        }
                signed = w3.eth.account.sign_transaction(tr, PRIVATE_KEY_TWO)
        
        tx = w3.eth.sendRawTransaction(signed.rawTransaction)    
        tx_receipt = w3.eth.waitForTransactionReceipt(tx)

        # TODO: I need to change the name to our contract name
        our_contract = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)
        st.write('Transaction Complete.')
