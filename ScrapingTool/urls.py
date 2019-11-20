from django.urls import path
from django.views.generic import RedirectView

from ScrapingTool.views import homepage_view, brand_view, mobile_view

favicon_view = RedirectView.as_view(url='/static/image/favicon.ico', permanent=True)
urlpatterns = [
    path('home/', homepage_view, name='home'),
    path('home/brand/', brand_view, name='brand/'),
    path('home/brand/mobiles/', mobile_view, name='mobiles/'),
    path('favicon\.ico', favicon_view)
]