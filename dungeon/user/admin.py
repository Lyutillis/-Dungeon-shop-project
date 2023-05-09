from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError

from .models import User, WishList
from django.utils.safestring import mark_safe
from django_admin_relation_links import AdminChangeLinksMixin

# Register your models here.
class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'username', 'profile_pic', 'is_active')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('email', 'password', 'username', 'profile_pic', 'is_active', 'is_superuser', 'is_staff')


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    change_form_template = 'admin/user/user_change_form.html'
    
    list_display = ('id', 'email', 'username', 'admin_image', 'is_active', 'is_staff', 'is_superuser')
    list_filter = ('is_active', 'is_staff', 'is_superuser',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('username','profile_pic', 'previewPicture')}),
        ('Permissions', {'fields': ('is_active', 'is_superuser', 'is_staff',)}),
    )

    def previewPicture(self, obj):
        return mark_safe('<img src="/static{url}" width="{width}" height={height} />'.format(
            url=obj.profile_pic.url,
            width=150,
            height=150,
        ))

    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'username', 'profile_pic','is_active'),
        }),
    )

    search_fields = ('email', 'username', 'id')
    ordering = ('email', 'username', 'is_active', 'is_staff', 'is_superuser', 'id',)
    readonly_fields=['previewPicture']

    def previewPicture(self, obj):
        return mark_safe('<img src="/static{url}" width="{width}" height={height} />'.format(
            url=obj.profile_pic.url,
            width=150,
            height=150,
        ))

class WishListAdmin(AdminChangeLinksMixin, admin.ModelAdmin):
    list_display=['id', 'product_link', 'user_link',]
    list_filter=[]
    ordering = ('id', 'product', 'user',)

    change_links=['product', 'user']

    search_fields=['id', 'user__name', 'user__id', 'user__email', 'product__name', 'product__id']

    def user_link_label(self, user):
        return '{} {}'.format(
            user.username,
            user.email,
        )

    def product_link_label(self, product):
        return '{}'.format(
            product.name,
        )


# Now register the new UserAdmin...
admin.site.register(User, UserAdmin)
# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.
admin.site.unregister(Group)
admin.site.register(WishList, WishListAdmin)