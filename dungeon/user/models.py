import sys
import pathlib
import uuid
from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import IntegrityError
from django.utils.html import mark_safe

def image_upload_handler(instance, filename) :
	fpath=pathlib.Path(filename)
	new_fname=str(uuid.uuid1())
	return f'profile-pics/{new_fname}{fpath.suffix}'

class UserManager(BaseUserManager) :

	def create_user(self, email, password, **extra_fields) :
		if not email :
			raise ValueError('The Email must be set')
		email = self.normalize_email(email)
		user = self.model(email=email, **extra_fields)
		user.set_password(password)
		try: 
			user.save()
		except IntegrityError :
			return None
		username='User'+str(user.id)
		user.update(username=username)
		return user

	def create_superuser(self, email, password, **extra_fields):
		extra_fields.setdefault('is_staff', True)
		extra_fields.setdefault('is_superuser', True)
		extra_fields.setdefault('is_active', True)
		return self.create_user(email, password, **extra_fields)

# Create your models here.
class User(AbstractBaseUser, PermissionsMixin) :
	class Meta:
		verbose_name_plural = "Users"

	email = models.CharField(max_length=100, unique=True)
	password=models.CharField(default=None, max_length=255)
	username = models.CharField(default=None, max_length=100, null=True)
	profile_pic = models.ImageField(default='profile-pics/default_pic.gif', upload_to=image_upload_handler, null=True)
	is_staff = models.BooleanField(default=False)
	is_superuser = models.BooleanField(default=False)
	is_active = models.BooleanField(default = True)
	id = models.AutoField(primary_key=True)

	USERNAME_FIELD = 'email'
	objects = UserManager()

# Class methods.

	@staticmethod
	def get_by_id(user_id):
		user = User.objects.filter(id=user_id).first()
		return user if user else None

	@staticmethod
	def get_by_email(email):
		user = User.objects.filter(email=email).first()
		return user if user else None

	@staticmethod
	def delete_by_id(user_id):
		user_to_delete = User.objects.filter(id=user_id).first()
		if user_to_delete:
			user_to_delete.delete()
			return True
		return False

	@staticmethod
	def create(email, password):
		if len(email) <= 100 and len(email.split('@')) == 2 and len(User.objects.filter(email=email)) == 0 :
			user = User(email=email, password=password)
			user.save()
			return user
		return None

	def to_dict(self):
		return {'id': self.id,
				'email': f'{self.email}',
				}

	def admin_image(self):
		return mark_safe('<img src="{}" width="100"/>'.format(self.profile_pic.url))
	admin_image.short_description = "Picture"
	admin_image.allow_tags = True

	def update(self, password=None, is_active=None, username=None, profile_description=None):
		user_to_update = User.objects.filter(email=self.email).first()
		if password != None:
			user_to_update.password = password
		if is_active != None:
			user_to_update.is_active = is_active
		if username!=None:
			user_to_update.username=username
		user_to_update.save()

	@staticmethod
	def get_all():
		return User.objects.all()

class WishList(models.Model):
	class Meta:
		verbose_name_plural = "Wish List"

	from product.models import Product

	user=models.ForeignKey(User, on_delete=models.CASCADE, null=False)
	product=models.ForeignKey(Product, on_delete=models.CASCADE, null=False)
	id = models.AutoField(primary_key=True)