from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required
def guest(request):
    return render(request, 'guest_interface.html')

@staff_member_required
def reception(request):
    return render(request, 'reception_interface.html')
