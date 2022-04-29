from django.contrib import admin

# Register your models here.
from .models import Card, GuestEntry
from operator import or_
from django.db.models import Q
from functools import reduce

@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    pass

@admin.register(GuestEntry)
class GuestEntryAdmin(admin.ModelAdmin):
    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super(GuestEntryAdmin, self).get_search_results(
                                               request, queryset, search_term)
        search_words = search_term.split()
        if search_words:
            q_objects = [Q(**{field + '__icontains': word})
                                for field in self.search_fields
                                for word in search_words]
            queryset |= self.model.objects.filter(reduce(or_, q_objects))
        return queryset, use_distinct

    # list_display = ("guest_first_name", "guest_last_name", "enter_datetime")
    list_filter = ("enter_datetime",)
    search_fields = ("guest_last_name", "guest_first_name", "company")
    # search_fields = ("guest_first_name__startswith", )
    list_display = ( "guest_first_name", "guest_last_name", "company", "keeper_full_name", "card", "enter_datetime", "exit_datetime")