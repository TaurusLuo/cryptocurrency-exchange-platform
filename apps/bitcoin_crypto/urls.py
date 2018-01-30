from django.conf.urls import url
from .views import ExchangeRateView, ConfirmView, TransactionListView,WalletsView


urlpatterns = [
    # url(r'^index/', IndexView.as_view(), name='index'),
    url(r'^exchange-rate/', ExchangeRateView.as_view(), name='exchange_rate'),
    url(r'^confirm/', ConfirmView.as_view(), name='confirm'),
    url(r'^transactions/', TransactionListView.as_view(), name='transaction_list'),
    url(r'^wallets/', WalletsView.as_view(), name='wallets'),


]