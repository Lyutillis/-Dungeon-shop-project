import sys
import pathlib
import uuid
from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import IntegrityError
from django.core.validators import MaxValueValidator, MinValueValidator


def product_image_upload_handler(instance, filename) :
	fpath=pathlib.Path(filename)
	new_fname=str(uuid.uuid1())
	return f'product-pics/{new_fname}{fpath.suffix}'

def supplier_image_upload_handler(instance, filename) :
	fpath=pathlib.Path(filename)
	new_fname=str(uuid.uuid1())
	return f'supplier-pics/{new_fname}{fpath.suffix}'

class Supplier(models.Model):

	name=models.CharField(default='No Title', max_length=1000)
	picture=models.ImageField(default='supplier-pics/default_pic.gif', upload_to=supplier_image_upload_handler, null=True)
	city=models.CharField(default='No Title', max_length=100)
	description=models.CharField(default='No Title', max_length=1000)
	rating=models.IntegerField(null=True, default=100, validators=[MaxValueValidator(100), MinValueValidator(1),])
	id = models.AutoField(primary_key=True)

# Create your models here.
class Product(models.Model) :

	name=models.CharField(default='No Title', max_length=1000)
	price=models.CharField(default='', max_length=10000)
	category=models.CharField(default='Undefined', max_length=10000)
	description=models.CharField(default=None, max_length=10000)
	picture=models.ImageField(default='product-pics/default_pic.gif', upload_to=product_image_upload_handler, null=True)
	supplier=models.ForeignKey(Supplier, on_delete=models.CASCADE)
	id = models.AutoField(primary_key=True)

# Class methods.

	@staticmethod
	def get_by_id(id):
		product=Product.objects.filter(id=id).first()
		return product if product else None

	"""@staticmethod
				def create(title=None, body=None, user_id=None):
					note = Note()
					if title:
						note.title = title
					if body:
						note.body = body
					if user_id :
						user=User.objects.filter(id=user_id).first()
						note.user=user	
					else :
						return False
					note.save()
					return note
			
				def update(self, title=None, body=None):
					if title is not None:
						self.title = title
			
					if body is not None:
						self.body = body
			
					self.save()"""