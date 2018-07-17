from django.conf.urls import url

from products.views import ProductListView
from .views import SearchProductView

urlpatterns = [
    url(r'^$', SearchProductView.as_view(), name='query')
]
