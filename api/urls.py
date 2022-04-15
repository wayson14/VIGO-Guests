
from django.urls import path, include

from api.models import GuestEntry
from .views import (
    CardView,
    GuestEntryView,
    GuestEntryDetailView
)

urlpatterns = [
    path('cards', CardView.as_view()),
    path('guest_entries', GuestEntryView.as_view()),
    path('guest_entries/<int:guest_entry_id>/', GuestEntryDetailView.as_view())
]