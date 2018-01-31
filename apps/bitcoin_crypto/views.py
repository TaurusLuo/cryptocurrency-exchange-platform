import random
import os
import hashlib
import hmac
import json
import requests
from decimal import Decimal
from twilio.rest import Client

from django.shortcuts import render, HttpResponse, render_to_response
from django.views.generic import TemplateView, FormView, View, ListView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.conf import settings

from apps.bitcoin_crypto.forms import TransactionForm
from apps.bitcoin_crypto.models import Transaction
from apps.bitcoin_crypto.utils import changelly_transaction
from apps.authentication.decorators import check_otp
from apps.authentication.models import AccessLog

CURRENCY = {
    '0': 'btc',
    '1': 'eth',
    '2': 'ltc',
    '3': 'xmr',
    '4': 'bch',
    '5': 'btg',

}


class IndexView(TemplateView):
    template_name = 'theme/index.html'


@method_decorator(login_required, name='dispatch')
@method_decorator(check_otp, name='dispatch')
class WelcomeView(TemplateView):
    template_name = 'welcome.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        logs = AccessLog.objects.filter(user=self.request.user)
        if len(logs)>2:
            context["last"] = logs[len(logs)-2] 
        return context


class ExchangeRateView(View):
    """
    Displaying the exchange rate based on the amount.
    If no amount entered will take the minimum transaction amount
    """
    def post(self, request, *args, **kwargs):
        convert_from = CURRENCY[request.POST.get('from')]
        convert_to = CURRENCY[request.POST.get('to')]
        amount = request.POST.get('amount')
        
        if amount:
            params =  {
                    "from": convert_from,
                    "to": convert_to,
                    "amount": amount
                }
            method = "getExchangeAmount"
        else:
            params =  {
                    "from": convert_from,
                    "to": convert_to,
                }
            method = 'getMinAmount'
        data = changelly_transaction(method,params)
        if not data.get('error'):
            request.session['convert_from'] = convert_from
            request.session['convert_to'] = convert_to
            request.session['amount'] = amount
            if not amount:
                request.session['amount'] = '1'
        return HttpResponse(json.dumps(data), content_type='application/json')

@method_decorator(login_required, name='dispatch')
@method_decorator(check_otp, name='dispatch')
class ConfirmView(FormView):
    """
    Create transaction
    """
    template_name = 'exchange_confirm.html'
    form_class = TransactionForm
    
    def post(self, *args, **kwargs):
        if self.request.POST.get('otp'):
            if self.request.session['confirm_otp'] == self.request.POST.get('otp'):
                address = self.request.session['address']
                del self.request.session['confirm_otp']
                del self.request.session['address']
                return render(self.request,'pay_in.html', {"address": address})
            else:
                pin = self._get_pin()
                self.request.session['confirm_otp'] = pin
                self.send_otp(pin,self.request.user.phone_number)
                return render(self.request,"authentication/otp.html")
        form = self.form_class(data=self.request.POST)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid()


    def form_valid(self, form):

        transaction_from = form.cleaned_data.get('transaction_from')
        convert_from = self.request.session['convert_from']
        convert_to = self.request.session['convert_to']
        amount = self.request.session['amount']
        params = {
                    "from": convert_from,
                    "to": convert_to,
                    "address": transaction_from,
                    "extraId": None,
                    "amount": amount
                  }
        data = changelly_transaction('createTransaction',params)
        if data.get('error'):
            return render(self.request,'exchange_confirm.html',{'error': data.get('error').get('message')})
        else:
            trans_obj = Transaction.objects.create( user = self.request.user,
                                                    from_currency =  convert_from,
                                                    to_currency = convert_to,
                                                    amount = Decimal(amount),
                                                    transaction_id = data['result'].get('id'),
                                                    transaction_from = data['result'].get('payoutAddress'),
                                                    transaction_to = data['result'].get('payinAddress')
                                                   )

            pin = self._get_pin()
            self.request.session['confirm_otp'] = pin
            self.request.session['address'] = trans_obj.transaction_to
            self.send_otp(pin,self.request.user.phone_number)
            return render(self.request,"authentication/otp.html")
            # return render(self.request,'pay_in.html', {"address": trans_obj.transaction_to})

    def send_otp(self,pin,number):
        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        message = client.messages.create(
                                body="Your verification code is %s" % pin,
                                to=number,
                                from_=settings.TWILIO_FROM_NUMBER,
                            )

    def _get_pin(self,length=5):
        """ Return a numeric PIN with length digits """
        return str(random.sample(range(10**(length-1), 10**length), 1)[0])

@method_decorator(login_required, name='dispatch')
@method_decorator(check_otp, name='dispatch')
class TransactionListView(ListView):
    """
    All transactions list of a user
    """
    model = Transaction
    template_name = 'transactions.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_list'] = self.object_list.filter(user=self.request.user)
        return context

@method_decorator(login_required, name='dispatch')
@method_decorator(check_otp, name='dispatch')
class WalletsView(TemplateView):
    template_name = 'wallets.html'