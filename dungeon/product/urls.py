from django.urls import path

from . import views

urlpatterns = [
	path(r'^product-page/(?P<id>[0-9]+)$', views.product_page_view, name='product-page'),
	path('update-item/', views.update_item, name='update-item'),
	path('checkout/', views.checkout, name='checkout'),
	path('cart/', views.cart_view, name='cart'),
	path('process-order/', views.processOrder, name='process-order'),
]