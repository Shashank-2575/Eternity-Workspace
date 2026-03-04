from django.http import HttpResponse
from django.shortcuts import render 

def home(request):
    return render(request, 'website/index.html')

def about(request):
    return HttpResponse("This is the about page.")

def contact(request):
    return HttpResponse("This is the contact page.")

def login(request):
    return render(request, 'website/login.html')    

def register(request):
    return render(request, 'website/register.html')    