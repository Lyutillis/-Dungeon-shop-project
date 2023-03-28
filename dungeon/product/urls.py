from django.urls import path

from . import views

urlpatterns = [
	path(r'^product-page/(?P<id>[0-9]+)$', views.product_page_view, name='product-page'),
]