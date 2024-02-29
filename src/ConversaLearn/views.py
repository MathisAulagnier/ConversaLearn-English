from decimal import ConversionSyntax
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate

def home(request):
    return render(request, 'home.html')

def chat(request):
    return render(request, 'chat.html')