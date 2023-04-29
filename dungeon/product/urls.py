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
	path('create-product/', views.createProduct, name='create-product'),
	path('create-category/', views.createCategory, name='create-category'),
	path('delete-category/', views.deleteCategory, name='delete-category'),
	path('create-subcategory/', views.createSubCategory, name='create-subcategory'),
	path('delete-subcategory/', views.deleteSubCategory, name='delete-subcategory'),
	path('create-product-ajax/', views.create_product_ajax, name='create-product-ajax'),
	path('edit-product/<int:id>', views.editProduct, name='edit-product'),
]