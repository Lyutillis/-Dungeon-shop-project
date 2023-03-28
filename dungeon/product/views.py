from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from user.models import User
from .models import Product
import os


def product_page_view(request, id) :
	product=Product.get_by_id(id)
	return render(request, 'product_page.html', {'product': product})