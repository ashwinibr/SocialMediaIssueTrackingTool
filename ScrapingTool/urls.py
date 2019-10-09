from django.urls import path
from django.views.generic import RedirectView

from ScrapingTool.views import homepage_view, product_view, series_view, brand_view, mobile_view

favicon_view = RedirectView.as_view(url='/static/image/favicon.ico', permanent=True)
urlpatterns = [
    path('home/', homepage_view, name='home'),
    path('home/brand/', brand_view, name='brand/'),
    path('home/brand/mobiles/', mobile_view, name='mobiles/'),
    path('home/series/', series_view, name='series/'),
    path('home/series/product/', product_view, name='product/'),
    path('favicon\.ico', favicon_view)

]