from django.contrib import admin
from .models import Product, Supplier, Order, OrderItem, ShippingAddress, Comment, ReplyComment, Reply

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin) :
	list_display=['id', 'name', 'price', 'description', 'category', 'picture', 'get_supplier']
	list_filter=['id', 'name', 'price', 'category']

	@admin.display(ordering="supplier__name", description="Supplier Name")
	def get_supplier(self, obj):
		return obj.supplier.name

	def get_readonly_fields(self, request, obj=None):
		if obj:
			return ('name', 'description')
		else:
			return ()

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin) :
	list_display=['id', 'name', 'picture', 'description', 'rating', 'city']
	list_filter=['id', 'name', 'rating', 'city']

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