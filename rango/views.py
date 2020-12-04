from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return HttpResponse('<a href="/rango/about/">About</a><br/>Rango says hey there partner!')


def about(requets):
    return HttpResponse('<a href="/rango/">Index</a><br/>Rango says here is the about page.')
