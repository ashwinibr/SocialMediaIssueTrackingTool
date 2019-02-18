from django.urls import path
from django.views.generic import RedirectView

from ScrapingTool.views import homepage_view, product_view, series_view, brand_view, mobile_view

favicon_view = RedirectView.as_view(url='/static/favicon.ico', permanent=True)
urlpatterns = [
    path('homepage/', homepage_view, name='homepage'),
    path('homepage/brand/', brand_view, name='brand/'),
    path('homepage/brand/mobiles/', mobile_view, name='mobiles/'),
    path('homepage/series/', series_view, name='series/'),
    path('homepage/series/product/', product_view, name='product/')

    #path('favicon\.ico', favicon_view),

]