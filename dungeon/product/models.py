import sys
import pathlib
import uuid
from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import IntegrityError
from django.core.validators import MaxValueValidator, MinValueValidator
from user.models import User
from django.utils.html import mark_safe

def product_image_upload_handler(instance, filename) :
	fpath=pathlib.Path(filename)
	new_fname=str(uuid.uuid1())
	return f'product-pics/{new_fname}{fpath.suffix}'

def supplier_image_upload_handler(instance, filename) :
	fpath=pathlib.Path(filename)
	new_fname=str(uuid.uuid1())
	return f'supplier-pics/{new_fname}{fpath.suffix}'

class Category(models.Model):
	class Meta:
		verbose_name_plural = "Categories"

	name=models.CharField(default='No Title', max_length=1000, null=False)
	id = models.AutoField(primary_key=True)

class SubCategory(models.Model):
	class Meta:
		verbose_name_plural = "SubCategories"

	category = models.ForeignKey(Category, on_delete=models.CASCADE, null=False)
	name=models.CharField(default='No Title', max_length=1000, null=False)
	id = models.AutoField(primary_key=True)

# Create your models here.
class Product(models.Model) :
	class Meta:
		verbose_name_plural = "Products"

	name=models.CharField(default='No Title', max_length=1000)
	price=models.DecimalField(max_digits = 8, decimal_places = 2, default=0)
	oldPrice=models.DecimalField(max_digits = 8, decimal_places = 2, default=0) 
	category=models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
	subcategory=models.ForeignKey(SubCategory, on_delete=models.CASCADE, null=True)
	description=models.CharField(default=None, max_length=10000)
	picture=models.ImageField(default='product-pics/default_pic.png', upload_to=product_image_upload_handler, null=True)
	id = models.AutoField(primary_key=True)

# Class methods.

	def admin_img(self):
		return mark_safe('<img src="{}" width="100"/>'.format(self.picture.url))
	admin_img.short_description = "Picture"
	admin_img.allow_tags = True

class Rating(models.Model):
	class Meta:
		verbose_name_plural = "Rating"

	id = models.AutoField(primary_key=True)
	quantity = models.IntegerField(default=0, validators=[MinValueValidator(0),])
	overall = models.DecimalField(default=5, max_digits = 10, decimal_places = 2)
	stars = models.IntegerField(default=0, validators=[MinValueValidator(0),])
	product=models.ForeignKey(Product, on_delete=models.CASCADE, null=False)

class Order(models.Model):
	class Meta:
		verbose_name_plural = "Orders"

	id = models.AutoField(primary_key=True)
	customer = models.ForeignKey(User, on_delete=models.CASCADE)
	date_ordered = models.DateTimeField(auto_now_add=True)
	complete = models.BooleanField(default=False, null=False)
	transaction_id = models.CharField(max_length=200, null=False)

	@property
	def get_cart_total(self):
		orderItems=self.orderitem_set.all()
		total = sum([i.get_total for i in orderItems])
		return total
	
	@property
	def get_cart_items(self):
		orderItems=self.orderitem_set.all()
		total = sum([i.quantity for i in orderItems])
		return total

class OrderItem(models.Model):
	class Meta:
		verbose_name_plural = "Order Items"

	product = models.ForeignKey(Product, on_delete=models.CASCADE, null=False)
	order=models.ForeignKey(Order, on_delete=models.CASCADE, null=False)
	quantity=models.IntegerField(default=1, null=False)
	date_added=models.DateTimeField(auto_now_add=True)

	@property
	def get_total(self):
		total = self.product.price * self.quantity
		return total

class ShippingAddress(models.Model):
	class Meta:
		verbose_name_plural = "Shipping Addresses"

	customer = models.ForeignKey(User, on_delete=models.CASCADE)
	order=models.ForeignKey(Order, on_delete=models.CASCADE, null=False)
	address = models.CharField(max_length=200, null=False)
	city = models.CharField(max_length=200, null=False)
	zipcode = models.CharField(max_length=200, null=False)
	date_added=models.DateTimeField(auto_now_add=True)

class Comment(models.Model):
	class Meta:
		verbose_name_plural = "Comments"

	product = models.ForeignKey(Product, on_delete=models.CASCADE)
	customer = models.ForeignKey(User, on_delete=models.CASCADE)
	body = models.CharField(max_length=1000, null=True)
	rating = models.IntegerField(default=0, validators=[MaxValueValidator(5), MinValueValidator(1),])

class ReplyComment(models.Model):
	class Meta:
		verbose_name_plural = "Reply Comments"

	customer = models.ForeignKey(User, on_delete=models.CASCADE)
	body = models.CharField(max_length=1000, null=False)

class Reply(models.Model):
	class Meta:
		unique_together = ("comment", "reply")
		verbose_name_plural = "Replies"

	comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
	reply = models.ForeignKey(ReplyComment, on_delete=models.CASCADE)

class PictureList(models.Model) :
	class Meta:
		verbose_name_plural = "Picture List"

	product = models.ForeignKey(Product, on_delete=models.CASCADE)
	picture1=models.ImageField(default='product-pics/default_pic.gif', upload_to=product_image_upload_handler, null=True)
	picture2=models.ImageField(default='product-pics/default_pic.gif', upload_to=product_image_upload_handler, null=True)
	picture3=models.ImageField(default='product-pics/default_pic.gif', upload_to=product_image_upload_handler, null=True)
	picture4=models.ImageField(default='product-pics/default_pic.gif', upload_to=product_image_upload_handler, null=True)
	picture5=models.ImageField(default='product-pics/default_pic.gif', upload_to=product_image_upload_handler, null=True)
	picture6=models.ImageField(default='product-pics/default_pic.gif', upload_to=product_image_upload_handler, null=True)