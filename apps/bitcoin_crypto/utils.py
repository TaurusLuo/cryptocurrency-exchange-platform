import hashlib
import hmac
import json
import requests
import subprocess

from bitcoin import *
from blockcypher import create_wallet_from_address
from cryptocurrency_wallet_generator import generate_wallet

from apps.authentication.models import Wallet
from apps.bitcoin_crypto.monero import *

API_URL = 'https://api.changelly.com'
API_KEY = ''
API_SECRET = ''
API_KEY_BLOCK = ''


def changelly_transaction(method, params):
    message = {
                  "jsonrpc": "2.0",
                  "method": method,
                  "params": params,
                  # {
                  #   "from": "ltc",
                  #   "to": "eth",
                  #   "address": "0x49f79352100bd92eb2ba3daa30852f03abdd8315",
                  #   "extraId": None,
                  #   "amount": 1
                  # },
                  "id": 1
                }

    serialized_data = json.dumps(message)

    sign = hmac.new(API_SECRET.encode('utf-8'), serialized_data.encode('utf-8'), hashlib.sha512).hexdigest()

    headers = {'api-key': API_KEY, 'sign': sign, 'Content-type': 'application/json'}
    response = requests.post(API_URL, headers=headers, data=serialized_data)

    return response.json()

def gen_address(user):
    priv = sha256(user.password)
    pub = privtopub(priv)
    addr = pubtoaddr(pub)
    return addr,pub,priv

def create_bitwallet(user):
    addr,pub,priv = gen_address(user)
    user.wallets.add(Wallet.objects.create(name='btc', address=addr, private=priv, public=pub))
    user.save()
    resp = create_wallet_from_address(wallet_name=user.username, address=addr, api_key=API_KEY_BLOCK)
    if resp.get("addresses"):
        return resp.get("addresses")[0]

    else:
      return None

def create_litewallet(user):
    process = subprocess.Popen(["/home/techversant/anandProjects/cryptocurrency_exchange/vanitygen/vanitygen","-X","48","Li"], stdout=subprocess.PIPE)
    result = process.communicate()[0].strip().decode('utf-8').split('\n')
    address = result[1].split("Address: ")[1]
    private_key = result[2].split("Privkey: ")[1]
    params = {
                "token": API_KEY_BLOCK,
                "name": user.username,
                "address": address
            }
    response = requests.post('https://api.blockcypher.com/v1/ltc/main/wallets',json=params)
    user.wallets.add(Wallet.objects.create(name='ltc', address=address, private=private_key))
    user.save()
    return address

def create_ethwallet(user):
    private_key,address = generate_wallet("Ethereum")
    user.wallets.add(Wallet.objects.create(name='eth', address=address, private=private_key))
    user.save()
    return address

def create_xmrwallet(user):
    words,pub,address,private_key = gen_new_wallet()
    single_word = ",".join(word for word in words)
    user.wallets.add(Wallet.objects.create(name='xmr', address=address, public=pub, private=private_key))
    user.save()
    return address
