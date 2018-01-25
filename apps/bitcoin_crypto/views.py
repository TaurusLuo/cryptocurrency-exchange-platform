import os
import hashlib
import hmac
import json
import requests
from decimal import Decimal

from django.shortcuts import render, HttpResponse, render_to_response
from django.views.generic import TemplateView, FormView, View, ListView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from apps.bitcoin_crypto.forms import TransactionForm
from apps.bitcoin_crypto.models import Transaction
from apps.bitcoin_crypto.utils import changelly_transaction
from apps.authentication.decorators import check_otp

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


class AboutView(TemplateView):
    template_name = 'about.html'


class IndexStatic(TemplateView):
    template_name = 'index-static.html'


class IndexSingle(TemplateView):
    template_name = 'index-single.html'


class ShortcodeWidgets(TemplateView):
    template_name = 'shortcodes_teasers.html'


class Services(TemplateView):
    template_name = 'services.html'


class ServicesSingle(TemplateView):
    template_name = 'service-single.html'


class GalleryRegular(TemplateView):
    template_name = 'gallery-regular.html'


class Timetable(TemplateView):
    template_name = 'timetable.html'


# class ExchangeView(TemplateView):
#     template_name = 'exchange.html'


class BlogRightView(TemplateView):
    template_name = 'blog-right.html'


class ShopRightView(TemplateView):
    template_name = 'shop-right.html'



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
    success_url = '/thanks/'

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
            return render(self.request,'pay_in.html', {"address": trans_obj.transaction_to})

@method_decorator(login_required, name='dispatch')
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
class WalletsView(TemplateView):
    template_name = 'wallets.html'