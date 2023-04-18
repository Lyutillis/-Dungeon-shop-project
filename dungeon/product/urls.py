from django.urls import path

from . import views

urlpatterns = [
	path('product-page/<int:id>', views.product_page_view, name='product-page'),
	path('update-item/', views.update_item, name='update-item'),
	path('checkout/', views.checkout, name='checkout'),
	path('cart/', views.cart_view, name='cart'),
	path('process-order/', views.processOrder, name='process-order'),
	path('publish-comment/<int:id>', views.publishComment, name='publish-comment'),
	path('publish-reply/<int:id>', views.publishReply, name='publish-reply'),
	path('user-list', views.user_list_view, name='user-list'),
	path('update-permission-superuser/', views.updatePermissionSuperuser, name='update-permission-superuser'),
	path('update-permission-staff/', views.updatePermissionStaff, name='update-permission-staff'),
]