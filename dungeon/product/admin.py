from django.contrib import admin
from .models import Product, Order, OrderItem, ShippingAddress, Comment, ReplyComment, Reply, Category, SubCategory, PictureList, Rating

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin) :
	list_display=['id', 'name', 'price', 'description', 'category', 'picture', 'subcategory']
	list_filter=['id', 'name', 'price', 'category', 'subcategory']

	def get_readonly_fields(self, request, obj=None):
		if obj:
			return ()
		else:
			return ()

admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)
admin.site.register(Comment)
admin.site.register(ReplyComment)
admin.site.register(Reply)
admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(PictureList)
admin.site.register(Rating)
