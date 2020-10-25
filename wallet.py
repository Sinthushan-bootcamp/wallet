import subprocess
import json
from constants import *
import os
from dotenv import load_dotenv
import pprint
from web3 import Web3
from web3.middleware import geth_poa_middleware
from eth_account import Account
from bit import PrivateKeyTestnet

load_dotenv()

w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)

def derive_wallets(coins,MNEMONIC,numderive):
    command = f'php hd-wallet-derive\hd-wallet-derive.php -g --numderive={numderive} --mnemonic="{MNEMONIC}" --cols=path,address,privkey,pubkey --coin={coins} --format=json'
    p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    output, err = p.communicate()
    p_status = p.wait()
    keys = json.loads(output)
    return keys

def priv_key_to_account(coin, priv_key):
    if coin == 'eth':
        return Account.privateKeyToAccount(priv_key)
    else:
        return PrivateKeyTestnet(priv_key)
    
def create_raw_tx(coin, account, to, amount):
    if coin = 'eth':
        gasEstimate = w3.eth.estimateGas(
            {"from": account.address, "to": to, "value": amount}
        )
        chainId = w3.eth.chainId
        return {
            "from": account.address,
            "to": to,
            "value": amount,
            "gasPrice": w3.eth.gasPrice,
            "gas": gasEstimate,
            "nonce": w3.eth.getTransactionCount(account.address),
        }
    else:
        return PrivateKeyTestnet.prepare_transaction(account.address, [(to, amount, coin)])

def send_tx(coin, account, to, amount):
    tx = create_raw_tx(coin, account, to, amount)
    signed_tx = account.sign_transaction(tx)
    if coin = 'eth':
        return w3.eth.sendRawTransaction(signed_tx.rawTransaction)
    else:
        return NetworkAPI.broadcast_tx_testnet(signed_tx)

numderive = 30 
MNEMONIC = os.environ.get("MNEMONIC")

BTC_addresses = derive_wallets(BTCTEST, MNEMONIC,numderive)
ETH_addresses = derive_wallets(ETH, MNEMONIC,numderive)

coins = {'btc-test':BTC_addresses , 'eth': ETH_addresses}

pprint.pprint(coins)
pprint.pprint(coins[ETH][8]['privkey'])