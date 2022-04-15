from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import Card, GuestEntry
from .serializers import Card, CardSerializer, GuestEntrySerializer
# Create your views here.
from .models import Card, GuestEntry

class CardView(APIView):
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
        # find card of specified id
        
        
        data = {
            'guest_full_name': request.data.get('guest_full_name'),
            'keeper_full_name': request.data.get('keeper_full_name'),
            'notes': request.data.get('notes'),
            'card': request.data.get('card'),
        }
        serializer = GuestEntrySerializer(data=data)
        if serializer.is_valid():
            card = Card.objects.get(pk = request.data.get('card'))
            if not card.is_given:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(f'Card of id {card.id} is already given.', status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GuestEntryDetailView(LoginRequiredMixin, APIView):
    # permission_classes = [permissions.IsAuthenticated]
    def get_object(self, guest_entry_id):
        '''
        Helper method to get the object with given guest_entry
        '''
        try:
            return GuestEntry.objects.get(id=guest_entry_id)
        except GuestEntry.DoesNotExist:
            return None

    # 3. Retrieve
    def get(self, request, guest_entry_id, *args, **kwargs):
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
        }
        serializer = GuestEntrySerializer(instance = guest_entry, data=data, partial = True)
        if serializer.is_valid():
            card = Card.objects.get(pk = request.data.get('card'))
            if not card.is_given:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(f'Card of id {card.id} is already given.', status=status.HTTP_400_BAD_REQUEST)

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