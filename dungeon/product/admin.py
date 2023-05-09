from django.contrib import admin
from .models import Product, Order, OrderItem, ShippingAddress, Comment, ReplyComment, Reply, Category, SubCategory, PictureList, Rating
from django_admin_relation_links import AdminChangeLinksMixin
from django import forms
from django.utils.safestring import mark_safe

class ReplyCommentModelForm(forms.ModelForm):
	body=forms.CharField(widget=forms.Textarea)

	class Meta:
		model=ReplyComment
		fields='__all__'

class CategoryAdmin(admin.ModelAdmin):
	list_display=['id', 'name']
	list_filter=['name']
	ordering = ('id', 'name')

	search_fields = ['id', 'name']

class OrderModelChoiceField(forms.ModelChoiceField):
	def label_from_instance(self, obj):
		return "Order #{}".format(obj.id)

class ProductModelChoiceField(forms.ModelChoiceField):
	def label_from_instance(self, obj):
		return "{}".format(obj.name)

class UserModelChoiceField(forms.ModelChoiceField):
	def label_from_instance(self, obj):
		return "{} {}".format(obj.username, obj.email)

class CategoryModelChoiceField(forms.ModelChoiceField):
	def label_from_instance(self, obj):
		return "{}".format(obj.name)

class SubCategoryModelChoiceField(forms.ModelChoiceField):
	def label_from_instance(self, obj):
		return "{}".format(obj.name)

class ProductAdminForm(forms.ModelForm):
	category=CategoryModelChoiceField(queryset=Category.objects.all())
	subcategory=SubCategoryModelChoiceField(queryset=SubCategory.objects.all())

	class Meta:
		model = Product
		fields='__all__'

class CommentAdminForm(forms.ModelForm):
	from user.models import User
	product = ProductModelChoiceField(queryset=Product.objects.all())
	customer = UserModelChoiceField(queryset=User.objects.all())

	class Meta:
		model = Comment
		fields='__all__'

class CommentAdmin(AdminChangeLinksMixin, admin.ModelAdmin):
	form=CommentAdminForm

	list_display=['id', 'product_link', 'customer_link', 'rating']
	list_filter=['rating']
	ordering = ('id', 'product', 'customer', 'rating')

	change_links=['product', 'customer']

	search_fields = ['id', 'product__id', 'product__name',  'customer__id', 'customer__email', 'customer__username', 'rating']

	def product_link_label(self, product):
		return '{}'.format(
			product.name,
		)

	def customer_link_label(self, customer):
		return '{} {}'.format(
			customer.username,
			customer.email,
		)

class OrderItemAdminForm(forms.ModelForm):
	product = ProductModelChoiceField(queryset=Product.objects.all())
	order = OrderModelChoiceField(queryset=Order.objects.all())

	class Meta:
		model = OrderItem
		fields='__all__'

class OrderAdminForm(forms.ModelForm):
	from user.models import User
	customer = UserModelChoiceField(queryset=User.objects.all())

	class Meta:
		model = Order
		fields='__all__'

class PictureListAdminForm(forms.ModelForm):
	product = ProductModelChoiceField(queryset=Product.objects.all())

	class Meta:
		model = PictureList
		fields='__all__'

class RatingAdminForm(forms.ModelForm):
	product = ProductModelChoiceField(queryset=Product.objects.all())

	class Meta:
		model = Rating
		fields='__all__'

class OrderItemAdmin(AdminChangeLinksMixin, admin.ModelAdmin):
	form=OrderItemAdminForm

	list_display=['id', 'product_link', 'order_link', 'quantity', 'date_added']
	list_filter=[]
	ordering = ('id', 'product', 'order', 'quantity', 'date_added')

	change_links=['product', 'order']

	search_fields = ['id', 'product__id', 'product__name',  'order__id']

	def product_link_label(self, product):
		return '{}'.format(
			product.name,
		)

	def order_link_label(self, order):
		return 'Order #{}'.format(
			order.id,
		)

class OrderAdmin(AdminChangeLinksMixin, admin.ModelAdmin):
	form=OrderAdminForm

	list_display=['id', 'customer_link', 'date_ordered', 'complete', 'transaction_id']
	list_filter=['complete']
	ordering = ('id', 'customer', 'date_ordered', 'complete')

	change_links=['customer']

	search_fields = ['id', 'customer__id', 'customer__email', 'customer__username', 'transaction_id']

	def customer_link_label(self, customer):
		return '{} {}'.format(
			customer.username,
			customer.email,
		)

class PictureListAdmin(AdminChangeLinksMixin, admin.ModelAdmin):
	form=PictureListAdminForm

	list_display=['id', 'product_link']
	list_filter=[]
	ordering = ('id', 'product')
	
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
		
	change_links=['product']

	search_fields = ['id', 'product__id', 'product__name',]

	fieldsets = [
		(
			None,
			{
				"fields": ['product', 'picture1', 'previewPicture1', 'picture2', 'previewPicture2', 'picture3', 'previewPicture3', 'picture4', 'previewPicture4', 'picture5', 'previewPicture5', 'picture6', 'previewPicture6'],
			},
		),
	]

	def product_link_label(self, product):
		return '{}'.format(
			product.name,
		)

class ProductAdmin(AdminChangeLinksMixin, admin.ModelAdmin) :
	form=ProductAdminForm

	list_display=['id', 'name', 'price', 'oldPrice', 'category_link', 'admin_img', 'subcategory_link']
	list_filter=['category', 'subcategory']
	ordering = ('id', 'name', 'price', 'oldPrice', 'category', 'subcategory')

	change_links=['category', 'subcategory']

	search_fields = ['id', 'name', 'description', 'category__name', 'subcategory__name']

	readonly_fields = ['admin_img', 'previewPicture']

	def previewPicture(self, obj):
		return mark_safe('<img src="/static{url}" width="{width}" height={height} />'.format(
			url=obj.picture.url,
			width=150,
			height=150,
		))

	change_form_template = 'admin/products/product_change_form.html'

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

	def category_link_label(self, category):
		return '{}'.format(
			category.name,
		)

	def subcategory_link_label(self, subcategory):
		return '{}'.format(
			subcategory.name,
		)

class RatingAdmin(AdminChangeLinksMixin, admin.ModelAdmin):
	form=RatingAdminForm

	list_display=['id', 'quantity', 'overall', 'stars', 'product_link']
	list_filter=[]
	ordering = ('id', 'quantity', 'overall', 'stars', 'product')

	change_links=['product']

	search_fields = ['id', 'product__name']

	def product_link_label(self, product):
		return '{}'.format(
			product.name,
		)

class ReplyAdmin(AdminChangeLinksMixin, admin.ModelAdmin):
	list_display=['id', 'comment_link', 'reply_link',]
	list_filter=[]
	ordering = ('id', 'comment', 'reply',)

	change_links=['comment', 'reply']

	search_fields = ['id',]

	readonly_fields=['comment', 'reply']

	def comment_link_label(self, comment):
		return 'Comment #{} on {} by {}: {} star(s)'.format(
			comment.id,
			comment.product.name,
			comment.customer.username,
			comment.rating,
		)

	def reply_link_label(self, reply):
		return 'Reply By {}'.format(
			reply.customer.username,
		)

class ReplyCommentAdmin(AdminChangeLinksMixin, admin.ModelAdmin):
	form=ReplyCommentModelForm

	list_display=['id', 'customer_link',]
	list_filter=[]
	ordering = ('id', 'customer',)

	change_links=['customer']

	search_fields = ['id', 'customer__email', 'customer__username', 'customer__id']

	readonly_fields=['customer',]

	def customer_link_label(self, customer):
		return '{} {}'.format(
			customer.username,
			customer.email,
		)

class ShippingAddressAdmin(AdminChangeLinksMixin, admin.ModelAdmin):
	list_display=['id', 'customer_link', 'order_link', 'address', 'city', 'zipcode', 'date_added']
	list_filter=[]
	ordering = ('id', 'customer', 'order', 'address', 'city', 'zipcode', 'date_added')

	change_links=['customer', 'order']

	readonly_fields=['customer', 'order']

	search_fields=['id', 'customer__email', 'customer__username', 'customer__id', 'order__id', 'address', 'city', 'zipcode']

	def customer_link_label(self, customer):
		return '{} {}'.format(
			customer.username,
			customer.email,
		)

	def order_link_label(self, order):
		return 'Order #{}'.format(
			order.id,
		)

class SubCategoryAdmin(AdminChangeLinksMixin, admin.ModelAdmin):
	list_display=['id', 'name', 'category_link',]
	list_filter=['category',]
	ordering = ('id', 'name', 'category',)

	change_links=['category']

	search_fields=['id', 'name', 'category__name', 'category__id',]

	def category_link_label(self, category):
		return '{}'.format(
			category.name,
		)

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
