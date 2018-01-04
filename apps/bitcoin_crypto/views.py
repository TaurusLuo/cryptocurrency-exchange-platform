import os
import hashlib
import hmac
import json
import requests

from django.shortcuts import render
from django.views.generic import TemplateView

# Create your views here.

API_URL = 'https://api.changelly.com'
API_KEY = os.environ.get('API_KEY')
API_SECRET = os.environ.get('API_SECRET')


class IndexView(TemplateView):
    template_name = 'index.html'


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


class ExchangeView(TemplateView):
    template_name = 'exchange.html'


class BlogRightView(TemplateView):
    template_name = 'blog-right.html'


class ShopRightView(TemplateView):
    template_name = 'shop-right.html'

def changelly_transaction():
    message = {
                  "jsonrpc": "2.0",
                  "method": "createTransaction",
                  "params": {
                    "from": "ltc",
                    "to": "eth",
                    "address": "0x49f79352100bd92eb2ba3daa30852f03abdd8315",
                    "extraId": None,
                    "amount": 1
                  },
                  "id": 1
                }

    serialized_data = json.dumps(message)

    sign = hmac.new(API_SECRET.encode('utf-8'), serialized_data.encode('utf-8'), hashlib.sha512).hexdigest()

    headers = {'api-key': API_KEY, 'sign': sign, 'Content-type': 'application/json'}
    response = requests.post(API_URL, headers=headers, data=serialized_data)

    print(response.json())