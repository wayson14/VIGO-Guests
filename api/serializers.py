# todo/todo_api/serializers.py
from rest_framework import serializers
from .models import Card, GuestEntry

# Validators

class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = '__all__'

class GuestEntrySerializer(serializers.ModelSerializer):
    def parse_datetime(self, datetime_to_parse):
        return datetime_to_parse.strftime("%Y-%m-%d %H:%M")
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if representation['enter_datetime']:
            representation['enter_datetime'] = self.parse_datetime(instance.enter_datetime)
        if representation['exit_datetime']:
            representation['exit_datetime'] = self.parse_datetime(instance.exit_datetime)
        return representation
    
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

class CardGivingSerializer(serializers.ModelSerializer):
    class Meta:
        model = GuestEntry
        fields = ['card']
