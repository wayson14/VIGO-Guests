from django.contrib import admin

# Register your models here.
class InterfaceAdmin(admin.AdminSite):
    site_header = 'Zaloguj się do Panelu Recepcyjnego VIGO'
    login_template = 'login.html'

interface_admin = InterfaceAdmin(name='InterfaceAdmin')