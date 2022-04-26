from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.mixins import UpdateModelMixin
from rest_framework.generics import GenericAPIView
from django.shortcuts import get_object_or_404
from datetime import datetime
from django.http import JsonResponse
from django.contrib.admin.views.decorators import staff_member_required

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from .models import Card, GuestEntry
from .serializers import Card, CardSerializer, GuestEntrySerializer, CardGivingSerializer
from .models import Card, GuestEntry 

class StaffRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff

class CardView(StaffRequiredMixin, APIView):
    def get(self, request, *args, **kwargs):
        '''
        List all the card items for given requested user
        '''
        cards = Card.objects.all()
        serializer = CardSerializer(cards, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        '''
        Create the Card with given data
        '''
        data = {
            'id': request.data.get('id'),  
            'is_given': request.data.get('is_given')
        }
        serializer = CardSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # def delete()

class GuestEntryView(APIView):
    @staff_member_required
    def get(self, request, *args, **kwargs):
        '''
        List all the GuestEntry objects
        '''
        guest_entries = GuestEntry.objects.all()
        serializer = GuestEntrySerializer(guest_entries, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    
    def post(self, request, *args, **kwargs):
        '''
        Create the GuestEntry with given data
        '''
    
        #send message to consumer 
        async def send_prompt():
            channel_layer = get_channel_layer()
            await print('CHANNEL LAYER', channel_layer)
            await channel_layer.send(
                "stream",
                {
                    'type': 'message',
                    'message': 'test'
                }
            )

        # find card of specified id
        if request.data.get('enter_datetime') == None:
            enter_datetime = datetime.now()
        else:
            enter_datetime = request.data.get('enter_datetime')
        data = {
            'guest_first_name': request.data.get('guest_first_name'),
            'guest_last_name': request.data.get('guest_last_name'),
            'keeper_full_name': request.data.get('keeper_full_name'),
            'notes': request.data.get('notes'),
            'card': request.data.get('card'),
            'company': request.data.get('company'),
            'enter_datetime': enter_datetime,
            'exit_datetime': request.data.get('exit_datetime')
        }
        serializer = GuestEntrySerializer(data=data)
        if serializer.is_valid():
            try:
                card = Card.objects.get(pk = request.data.get('card'))
            except Card.DoesNotExist:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                if not card.is_given:
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                else:
                    return Response(f'Card of id {card.id} is already given.', status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CardDetailView(StaffRequiredMixin, APIView):
    def get_object(self, card_id):
        '''
        Helper method to get the object with given card_id
        '''
        try:
            return Card.objects.get(id=card_id)
        except Card.DoesNotExist:
            return None
            
    def get(self, request, card_id):
        card = self.get_object(card_id)
        if not card:
            return Response(
                {"res": "Object with card_id does not exist"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = CardSerializer(card)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, card_id):
  
        card = self.get_object(card_id)
        if not card:
            return Response(
                {"res": "Object with card_id does not exists"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        data = {
            'id': request.data.get('id'),
            'is_given': request.data.get('is_given'),
        }
        serializer = CardSerializer(instance = card, data=data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    def delete(self, request, card_id):
        card = self.get_object(card_id)
        if not card:
            return Response(
                {"res": "Object with card_id does not exists"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        card.delete()
        return Response(
            {"res": "Object deleted!"},
            status=status.HTTP_200_OK
        )

class GuestEntryDetailView(StaffRequiredMixin, APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get_object(self, guest_entry_id):
        '''
        Helper method to get the object with given guest_entry
        '''
        try:
            return GuestEntry.objects.get(id=guest_entry_id)
        except GuestEntry.DoesNotExist:
            return None

    # 3. Retrieve
    def get(self, request, guest_entry_id):
        '''
        Retrieves the Todo with given guest_entry
        '''
        guest_entry = self.get_object(guest_entry_id)
        if not guest_entry:
            return Response(
                {"res": "Object with todo id does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = GuestEntrySerializer(guest_entry)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 4. Update
    def put(self, request, guest_entry_id, *args, **kwargs):
        '''
        Updates the guest_entry item with given if exists
        '''
        guest_entry = self.get_object(guest_entry_id)
        if not guest_entry:
            return Response(
                {"res": "Object with guest_entry_id does not exists"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        data = {
            'guest_full_name': request.data.get('guest_full_name'),
            'keeper_full_name': request.data.get('keeper_full_name'),
            'notes': request.data.get('notes'),
            'card': request.data.get('card'),
            'company': request.data.get('company'),
            'enter_datetime': request.data.get('enter_datetime'),
            'exit_datetime': request.data.get('exit_datetime')
        }
        serializer = GuestEntrySerializer(instance = guest_entry, data=data, partial = True)
        if serializer.is_valid():
            try:
                card = Card.objects.get(pk = request.data.get('card'))
            except Card.DoesNotExist:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                if not card.is_given:
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                else:
                    return Response(f'Card of id {card.id} is already given.', status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # 5. Delete
    def delete(self, request, guest_entry_id, *args, **kwargs):
        '''
        Deletes the guest_entry item with given if exists
        '''
        guest_entry = self.get_object(guest_entry_id)
        if not guest_entry:
            return Response(
                {"res": "Object with guest_entry_id does not exists"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        guest_entry.delete()
        return Response(
            {"res": "Object deleted!"},
            status=status.HTTP_200_OK
        )

class GuestEntryGiveCard(StaffRequiredMixin, GenericAPIView, UpdateModelMixin):
    queryset = GuestEntry.objects.all()
    serializer_class = CardGivingSerializer
    def put(self, request, *args, **kwargs):
        return self.partial_update(request)

class GiveCard(APIView):
    def get(self, request, ge_id, card_id):
        guest_entry = get_object_or_404(GuestEntry, pk=ge_id)
        card = get_object_or_404(Card, pk = card_id)
        if guest_entry.card != None:
            return JsonResponse({"guest_entry": f"GuestEntry {ge_id} has already been assigned with Card {guest_entry.card.id} "}, status=400)
        elif card.is_given == True:
            return JsonResponse({"card": f"Card {card_id} has already been given to other guest!"}, status=400)
        else:
            guest_entry.card = card
            card.is_given = True
            guest_entry.save()
            card.save()
        
        return JsonResponse({"success": f"GuestEntry {ge_id} has been given Card {card_id}"})





class NoCardsGuests(StaffRequiredMixin, APIView):
    def get(self, request, *args, **kwargs):
        guest_entries = GuestEntry.objects.filter(card=None)
        serializer = GuestEntrySerializer(guest_entries, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class FreeCards(StaffRequiredMixin, APIView):
    def get(self, request):
        # active_guest_entries = GuestEntry.objects.filter(exit_datetime=None).exclude(card=None)
        # cards = []
        c = Card.objects.filter(is_given = False)
        cards = list(c)
        # for entry in active_guest_entries:
        #     if entry.card != None:
        #         if entry.card.is_given == False:
        #             cards.append(entry.card)
        # for entry in active_guest_entries
        # active_guest_entries = list(active_guest_entries)
        serializer = CardSerializer(cards, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ActiveGuestEntries(StaffRequiredMixin, APIView):
    def get(self, request):
        active_guest_entries = GuestEntry.objects.filter(exit_datetime=None).exclude(card=None)
        serializer = GuestEntrySerializer(active_guest_entries, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class CloseGuestEntry(StaffRequiredMixin, APIView):
    def get(self, request, guest_entry_id):
        guest_entry = get_object_or_404(GuestEntry, pk=guest_entry_id)
        card = guest_entry.card
        card.is_given = False
        card.save()
        guest_entry.exit_datetime = datetime.now()
        guest_entry.save()

        return Response( status=status.HTTP_200_OK)

class DiscardGuestEntry(StaffRequiredMixin, APIView):
    permission_classes = [permissions.IsAuthenticated]
    def delete(self, request, guest_entry_id):
        guest_entry = get_object_or_404(GuestEntry, pk=guest_entry_id)
        if guest_entry.card == None:
            guest_entry.delete()
        else:
            return JsonResponse({"GuestEntry":"Has a card."}, status=status.HTTP_400_BAD_REQUEST)
        return JsonResponse({"GuestEntry":"Has been deleted"}, status=status.HTTP_200_OK)