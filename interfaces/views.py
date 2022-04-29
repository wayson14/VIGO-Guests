from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import redirect
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import login, logout
# @staff_member_required
def guest(request):
    return render(request, 'guest_interface.html')

@staff_member_required
def reception(request):
    return render(request, 'reception_interface.html')

def panel(request):
    return render(request, 'panel.html')
def logout_view(request):
    logout(request)
    return redirect("/reception")