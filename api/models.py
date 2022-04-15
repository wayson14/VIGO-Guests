from django.db import models

# Create your models here.
class Card(models.Model):
    id              = models.IntegerField(primary_key=True, unique=True, null=False)
    is_given        = models.BooleanField(default=False)

class GuestEntry(models.Model):
    guest_full_name = models.CharField(max_length=100, blank=False)
    company         = models.CharField(max_length=100, null=True)
    enter_datetime  = models.DateTimeField(auto_now_add=True)
    exit_datetime   = models.DateTimeField(null=True)
    keeper_full_name= models.CharField(max_length=100, blank=False)
    notes           = models.CharField(max_length=1000, null=True, blank=True)
    card            = models.ForeignKey(Card, null=True, on_delete=models.DO_NOTHING)
    
