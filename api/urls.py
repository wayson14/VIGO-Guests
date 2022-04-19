
from django.urls import path, include

from api.models import GuestEntry
from .views import (
    CardDetailView,
    CardView,
    GuestEntryView,
    GuestEntryDetailView,
    GuestEntryGiveCard,
    NoCards,
)

urlpatterns = [
    path('cards', CardView.as_view()),
    path('guest_entries', GuestEntryView.as_view()),
    path('guest_entries/<int:guest_entry_id>/', GuestEntryDetailView.as_view()),
    path('guest_entries/<int:pk>/give_card', GuestEntryGiveCard.as_view()),
    path('cards/<int:card_id>/', CardDetailView.as_view()),
    path('no_cards', NoCards.as_view()),
]