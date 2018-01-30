"""cryptocurrency URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include, static
from django.contrib import admin
from django.conf import settings
from django.views.generic.base import TemplateView
from django.contrib.auth.decorators import login_required

from apps.bitcoin_crypto.views import IndexView, WelcomeView


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^crypto/', include('apps.bitcoin_crypto.urls')),
    url(r'^auth/', include('apps.authentication.urls')),
    url(r'^welcome/', WelcomeView.as_view(), name='welcome'),
    url(r'^exchange/', TemplateView.as_view(template_name='theme/exchange.html'), name='exchange'),
    url(r'^$', IndexView.as_view(), name='index'),

]

urlpatterns += static.static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static.static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
