from django.shortcuts import render
from django.views.generic import TemplateView


# Create your views here.

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
