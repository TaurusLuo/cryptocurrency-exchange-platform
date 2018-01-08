from django import template
from apps.bitcoin_crypto.utils import changelly_transaction

register = template.Library()

@register.simple_tag
def transaction_status(trans_id):
    params = {"id": trans_id}
     
    data = changelly_transaction('getStatus', params)
    if data.get('error'):
    	return "Payment not received.Failed."
    else:
    	return data.get('result')