from django.contrib import admin
from .models import Product, Order, OrderItem, ShippingAddress, Comment, ReplyComment, Reply 
"""Category, SubCategory"""

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin) :
	list_display=['id', 'name', 'price', 'description', 'picture', 'get_supplier']
	list_filter=['id', 'name', 'price', ]

	@admin.display(ordering="supplier__name", description="Supplier Name")
	def get_supplier(self, obj):
		return obj.supplier.name

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
"""admin.site.register(Category)
admin.site.register(SubCategory)"""