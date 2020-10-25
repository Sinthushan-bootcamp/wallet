import subprocess
import json
from constants import *
import os
from dotenv import load_dotenv
import pprint
load_dotenv()

numderive = 30 
MNEMONIC = os.environ.get("MNEMONIC")

def derive_wallets(coins,MNEMONIC,numderive):
    command = f'php hd-wallet-derive\hd-wallet-derive.php -g --numderive={numderive} --mnemonic="{MNEMONIC}" --cols=path,address,privkey,pubkey --coin={coins} --format=json'
    p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    output, err = p.communicate()
    p_status = p.wait()
    keys = json.loads(output)
    return keys
   
BTC_addresses = derive_wallets(BTCTEST, MNEMONIC,numderive)
ETH_addresses = derive_wallets(ETH, MNEMONIC,numderive)

coins = {'btc-test':BTC_addresses , 'eth': ETH_addresses}

pprint.pprint(coins)
pprint.pprint(coins[ETH][8]['privkey'])