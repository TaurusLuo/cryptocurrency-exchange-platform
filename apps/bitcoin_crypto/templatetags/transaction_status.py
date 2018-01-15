import json
import requests

from django import template
from apps.bitcoin_crypto.utils import changelly_transaction
from blockcypher import get_address_overview

register = template.Library()

@register.simple_tag
def transaction_status(trans_id):
    params = {"id": trans_id}
     
    data = changelly_transaction('getStatus', params)
    if data.get('error'):
        return "Payment not received.Failed."
    else:
        return data.get('result')

@register.simple_tag
def get_bit_balance(address, user):
    bal = get_address_overview(address)
    return bal['balance']
    
@register.simple_tag
def get_eth_balance(address):
    bal_req = requests.get("https://api.ethplorer.io/getAddressInfo/"+address+"?apiKey=freekey").text
    bal = json.loads(bal_req)
    return bal['ETH']['balance']
