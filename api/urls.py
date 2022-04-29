
from django.urls import path, include

from api.models import GuestEntry
from .views import (
    CardDetailView,
    CardView,
    DiscardGuestEntry,
    GuestEntryView,
    GuestEntryDetailView,
    # GuestEntryGiveCard,
    NoCardsGuests,
    FreeCards,
    ActiveGuestEntries,
    CloseGuestEntry,
    GiveCard
)

from .importer import Importer

urlpatterns = [
    path('cards', CardView.as_view()),
    path('guest_entries', GuestEntryView.as_view()),
    path('guest_entries/<int:guest_entry_id>/', GuestEntryDetailView.as_view()),
    path('guest_entries/<int:ge_id>/give_card/<int:card_id>', GiveCard.as_view()),
    path('guest_entries/<int:guest_entry_id>/close_entry', CloseGuestEntry.as_view()),
    path('guest_entries/<int:guest_entry_id>/discard_entry', DiscardGuestEntry.as_view()),
    path('cards/<int:card_id>/', CardDetailView.as_view()),
    path('no_cards_guests', NoCardsGuests.as_view()),
    path('free_cards', FreeCards.as_view()),
    path('active_guest_entries', ActiveGuestEntries.as_view()),
    path('import', Importer.as_view())
]