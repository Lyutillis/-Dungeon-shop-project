from django.urls import path

from . import views

urlpatterns = [
	path('', views.homepage_view, name='homepage'),
	path('login/', views.login_view, name='login'),
	path('logout/', views.logout_view, name='logout'),
	path('register/', views.register_view, name='register'),
	path('profile/', views.profile_view, name='profile'),
	path('add-to-wishlist/', views.addWishlist, name='add-to-wishlist'),
	path('remove-from-wishlist/', views.removeWishlist, name='remove-from-wishlist'),
	path('wishlist/', views.wishlist_view, name='wishlist')
]