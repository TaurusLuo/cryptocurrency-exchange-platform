from django.conf.urls import url
from .views import  AboutView, IndexStatic, IndexSingle, ShortcodeWidgets, Services, ServicesSingle, \
    GalleryRegular, Timetable, BlogRightView, ShopRightView, ExchangeRateView, ConfirmView, TransactionListView,\
    WalletsView


urlpatterns = [
    # url(r'^index/', IndexView.as_view(), name='index'),
    url(r'^about/', AboutView.as_view(template_name='about.html'), name='about'),
    url(r'^index-static/', IndexStatic.as_view(), name='index_static'),
    url(r'^index-single/', IndexSingle.as_view(), name='index_single'),
    url(r'^shortcode-widgets/', ShortcodeWidgets.as_view(), name='shortcode_widgets'),
    url(r'^services/', Services.as_view(), name='services'),
    url(r'^services-single/', ServicesSingle.as_view(), name='services_single'),
    url(r'^gallery-regular/', GalleryRegular.as_view(), name='gallery_regular'),
    url(r'^timetable/', Timetable.as_view(), name='timetable'),
    url(r'^blog-right/', BlogRightView.as_view(), name='blog_right'),
    url(r'^shop-right/', ShopRightView.as_view(), name='shop_right'),
    url(r'^exchange-rate/', ExchangeRateView.as_view(), name='exchange_rate'),
    url(r'^confirm/', ConfirmView.as_view(), name='confirm'),
    url(r'^transactions/', TransactionListView.as_view(), name='transaction_list'),
    url(r'^wallets/', WalletsView.as_view(), name='wallets'),


]