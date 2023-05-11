from django import forms
from user.models import User
from .models import Product, Order, OrderItem, ShippingAddress, Comment, ReplyComment, Reply, Category, SubCategory, PictureList, Rating

def product_link_label(self, product):
		return '{}'.format(
			product.name,
		)

def customer_link_label(self, customer):
    return '{} {}'.format(
        customer.username,
        customer.email,
    )

def order_link_label(self, order):
    return 'Order #{}'.format(
        order.id,
    )

def category_link_label(self, category):
    return '{}'.format(
        category.name,
    )

def subcategory_link_label(self, subcategory):
    return '{}'.format(
        subcategory.name,
    )

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

class ReplyCommentAdminForm(forms.ModelForm):
	body=forms.CharField(widget=forms.Textarea)

	class Meta:
		model=ReplyComment
		fields='__all__'

class ProductAdminForm(forms.ModelForm):
	category=CategoryModelChoiceField(queryset=Category.objects.all())
	subcategory=SubCategoryModelChoiceField(queryset=SubCategory.objects.all())

	class Meta:
		model = Product
		fields='__all__'

class CommentAdminForm(forms.ModelForm):
	product = ProductModelChoiceField(queryset=Product.objects.all())
	customer = UserModelChoiceField(queryset=User.objects.all())

	class Meta:
		model = Comment
		fields='__all__'

class OrderItemAdminForm(forms.ModelForm):
	product = ProductModelChoiceField(queryset=Product.objects.all())
	order = OrderModelChoiceField(queryset=Order.objects.all())

	class Meta:
		model = OrderItem
		fields='__all__'

class OrderAdminForm(forms.ModelForm):
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
