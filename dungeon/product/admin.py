from django.contrib import admin
from .models import Product, Order, OrderItem, ShippingAddress, Comment, ReplyComment, Reply, Category, SubCategory

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin) :
	list_display=['id', 'name', 'price', 'description', 'category', 'picture']
	list_filter=['id', 'name', 'price', 'category']

	def get_readonly_fields(self, request, obj=None):
		if obj:
			return ('name', 'description')
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