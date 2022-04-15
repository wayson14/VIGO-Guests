from django.contrib import admin

# Register your models here.
from .models import Card, GuestEntry

@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    pass

@admin.register(GuestEntry)
class GuestEntryAdmin(admin.ModelAdmin):
    pass