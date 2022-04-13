from django.shortcuts import render
from django.http import HttpResponse

def guest(request):
    return render(request, 'guest_interface.html')

def reception(request):
    return render(request, 'reception_interface.html')
