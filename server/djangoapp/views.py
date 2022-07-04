from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404, render, redirect
# from .models import CarModel, CarMake
from .restapis import get_dealers_from_cf, get_dealer_by_id_from_cf, get_reviews_by_dealer_id_from_cf
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

logger = logging.getLogger(__name__)


def about(request):
    return render(request, 'djangoapp/about.html')


def contact(request):
    return render(request, 'djangoapp/contact.html')


def login_request(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['psw']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('djangoapp:index')
        else:
            context = {
                'error': f'Login failed, please check your credentials.'
            }
            return render(request, 'djangoapp/error.html', context)


def logout_request(request):
    logout(request)
    return redirect('djangoapp:index')


def register(request):
    if request.user.is_authenticated:
        context = {
            'error': f'You are already logged in as "{request.user.username}"! Please log out to create a new account.'
        }
        return render(request, 'djangoapp/error.html', context)
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        try:
            User.objects.get(username=username)
        except ObjectDoesNotExist:
            user = User.objects.create_user(
                username=username,
                password=password,
                first_name=first_name,
                last_name=last_name)
            login(request, user)
            return redirect('djangoapp:index')
        context = {
            'error': f'User with name "{username}" is already registered, please try another name'
        }
        return render(request, 'djangoapp/registration.html', context)
    else:
        return render(request, 'djangoapp/registration.html')


def get_dealerships(request):
    context = {}
    if request.method == "GET":
        url = '/dealership'
        dealerships = get_dealers_from_cf(url)
        context['dealerships'] = dealerships
        return render(request, 'djangoapp/index.html', context)


def get_dealer_details(request, dealer_id):
    context = {}
    if request.method == "GET":
        url = '/dealership'
        dealer = get_dealer_by_id_from_cf(url, dealer_id)
        context['dealer'] = dealer
        url = '/review'
        reviews = get_reviews_by_dealer_id_from_cf(url, dealer_id)
        context['reviews'] = reviews
        return render(request, 'djangoapp/dealer_details.html', context)
