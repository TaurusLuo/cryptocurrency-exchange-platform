from django import forms
from apps.bitcoin_crypto.models import Transaction

class TransactionForm(forms.Form):
    transaction_from = forms.CharField()

    class Meta:
        model = Transaction
        fields = ['from_currency', 'to_currency', 'amount', 'transaction_from']