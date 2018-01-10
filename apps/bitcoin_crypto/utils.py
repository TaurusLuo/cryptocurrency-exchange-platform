import hashlib
import hmac
import json
import requests

from bitcoin import *
from blockcypher import create_wallet_from_address

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

def create_bitwallet(user):
    priv = sha256(user.password)
    pub = privtopub(priv)
    addr = pubtoaddr(pub)
    resp = create_wallet_from_address(wallet_name=user.username, address=addr, api_key=API_KEY_BLOCK)
    if resp.get("addresses"):
        return resp.get("addresses")[0]
    else:
      return None