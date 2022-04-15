# todo/todo_api/serializers.py
from rest_framework import serializers
from .models import Card, GuestEntry

# Validators

class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = '__all__'

class GuestEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = GuestEntry
        fields = '__all__'

        # def validate_card(self, value):
        #     card_id = value
        #     card = Card.objects.get(pk = card_id)
        #     if card.is_given:
        #         raise serializers.ValidationError('Card must not be given!')
    # validators = [
    #     card_is_not_given(data['card'])
    # ]

