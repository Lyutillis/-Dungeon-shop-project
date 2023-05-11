from django.contrib import admin
from .models import Product, Order, OrderItem, ShippingAddress, Comment, ReplyComment, Reply, Category, SubCategory, PictureList, Rating
from django_admin_relation_links import AdminChangeLinksMixin
from django import forms
from django.utils.safestring import mark_safe
from .forms import reply_link_label, comment_link_label, subcategory_link_label, category_link_label, order_link_label, customer_link_label, product_link_label, ProductAdminForm, OrderAdminForm, OrderItemAdminForm, CommentAdminForm, ReplyCommentAdminForm, PictureListAdminForm, RatingAdminForm

class CategoryAdmin(admin.ModelAdmin):
	list_display=['id', 'name']
	list_filter=['name']
	ordering = ('id', 'name')

	search_fields = ['id', 'name']

class CommentAdmin(AdminChangeLinksMixin, admin.ModelAdmin):
	form=CommentAdminForm

	list_display=['id', 'product_link', 'customer_link', 'rating']
	list_filter=['rating']
	ordering = ('id', 'product', 'customer', 'rating')

	change_links=['product', 'customer']

	search_fields = ['id', 'product__id', 'product__name',  'customer__id', 'customer__email', 'customer__username', 'rating']

class OrderItemAdmin(AdminChangeLinksMixin, admin.ModelAdmin):
	form=OrderItemAdminForm

	list_display=['id', 'product_link', 'order_link', 'quantity', 'date_added']
	list_filter=[]
	ordering = ('id', 'product', 'order', 'quantity', 'date_added')

	change_links=['product', 'order']

	search_fields = ['id', 'product__id', 'product__name',  'order__id']

class OrderAdmin(AdminChangeLinksMixin, admin.ModelAdmin):
	form=OrderAdminForm

	list_display=['id', 'customer_link', 'date_ordered', 'complete', 'transaction_id']
	list_filter=['complete']
	ordering = ('id', 'customer', 'date_ordered', 'complete')

	change_links=['customer']

	search_fields = ['id', 'customer__id', 'customer__email', 'customer__username', 'transaction_id']

class PictureListAdmin(AdminChangeLinksMixin, admin.ModelAdmin):
	form=PictureListAdminForm

	list_display=['id', 'product_link']
	list_filter=[]
	ordering = ('id', 'product')
	
	change_links=['product']

	search_fields = ['id', 'product__id', 'product__name',]

	readonly_fields = ['previewPicture1', 'previewPicture2', 'previewPicture3', 'previewPicture4', 'previewPicture5', 'previewPicture6']

	change_form_template = 'admin/picturelists/picturelists_change_form.html'

	def previewPicture1(self, obj):
		return mark_safe('<img src="/static{url}" width="{width}" height={height} />'.format(
			url=obj.picture1.url,
			width=150,
			height=150,
		))

	def previewPicture2(self, obj):
		return mark_safe('<img src="/static{url}" width="{width}" height={height} />'.format(
			url=obj.picture2.url,
			width=150,
			height=150,
		))

	def previewPicture3(self, obj):
		return mark_safe('<img src="/static{url}" width="{width}" height={height} />'.format(
			url=obj.picture3.url,
			width=150,
			height=150,
		))
	
	def previewPicture4(self, obj):
		return mark_safe('<img src="/static{url}" width="{width}" height={height} />'.format(
			url=obj.picture4.url,
			width=150,
			height=150,
		))
	
	def previewPicture5(self, obj):
		return mark_safe('<img src="/static{url}" width="{width}" height={height} />'.format(
			url=obj.picture5.url,
			width=150,
			height=150,
		))
	
	def previewPicture6(self, obj):
		return mark_safe('<img src="/static{url}" width="{width}" height={height} />'.format(
			url=obj.picture6.url,
			width=150,
			height=150,
		))
		

	fieldsets = [
		(
			None,
			{
				"fields": ['product', 'picture1', 'previewPicture1', 'picture2', 'previewPicture2', 'picture3', 'previewPicture3', 'picture4', 'previewPicture4', 'picture5', 'previewPicture5', 'picture6', 'previewPicture6'],
			},
		),
	]

class ProductAdmin(AdminChangeLinksMixin, admin.ModelAdmin) :
	form=ProductAdminForm

	list_display=['id', 'name', 'price', 'oldPrice', 'category_link', 'admin_img', 'subcategory_link']
	list_filter=['category', 'subcategory']
	ordering = ('id', 'name', 'price', 'oldPrice', 'category', 'subcategory')

	change_links=['category', 'subcategory']

	search_fields = ['id', 'name', 'description', 'category__name', 'subcategory__name']

	readonly_fields = ['admin_img', 'previewPicture']

	change_form_template = 'admin/products/product_change_form.html'

	def previewPicture(self, obj):
		return mark_safe('<img src="/static{url}" width="{width}" height={height} />'.format(
			url=obj.picture.url,
			width=150,
			height=150,
		))

	fieldsets = [
		(
			'Overall',
			{
				"fields": ['name', 'picture', 'previewPicture', 'price', 'oldPrice', 'description'],
			},
		),
		(
			'Categories',
			{
				"fields": ['category', 'subcategory'],
			},
		),
	]

class RatingAdmin(AdminChangeLinksMixin, admin.ModelAdmin):
	form=RatingAdminForm

	list_display=['id', 'quantity', 'overall', 'stars', 'product_link']
	list_filter=[]
	ordering = ('id', 'quantity', 'overall', 'stars', 'product')

	change_links=['product']

	search_fields = ['id', 'product__name']

class ReplyAdmin(AdminChangeLinksMixin, admin.ModelAdmin):
	list_display=['id', 'comment_link', 'reply_link',]
	list_filter=[]
	ordering = ('id', 'comment', 'reply',)

	change_links=['comment', 'reply']

	search_fields = ['id',]

	readonly_fields=['comment', 'reply']

class ReplyCommentAdmin(AdminChangeLinksMixin, admin.ModelAdmin):
	form=ReplyCommentAdminForm

	list_display=['id', 'customer_link',]
	list_filter=[]
	ordering = ('id', 'customer',)

	change_links=['customer']

	search_fields = ['id', 'customer__email', 'customer__username', 'customer__id']

	readonly_fields=['customer',]

class ShippingAddressAdmin(AdminChangeLinksMixin, admin.ModelAdmin):
	list_display=['id', 'customer_link', 'order_link', 'address', 'city', 'zipcode', 'date_added']
	list_filter=[]
	ordering = ('id', 'customer', 'order', 'address', 'city', 'zipcode', 'date_added')

	change_links=['customer', 'order']

	search_fields=['id', 'customer__email', 'customer__username', 'customer__id', 'order__id', 'address', 'city', 'zipcode']

	readonly_fields=['customer', 'order']

class SubCategoryAdmin(AdminChangeLinksMixin, admin.ModelAdmin):
	list_display=['id', 'name', 'category_link',]
	list_filter=['category',]
	ordering = ('id', 'name', 'category',)

	change_links=['category']

	search_fields=['id', 'name', 'category__name', 'category__id',]

admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(ShippingAddress, ShippingAddressAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(ReplyComment, ReplyCommentAdmin)
admin.site.register(Reply, ReplyAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(SubCategory, SubCategoryAdmin)
admin.site.register(PictureList, PictureListAdmin)
admin.site.register(Rating, RatingAdmin)
