from django.db import models

# Create your models here.
class Card(models.Model):
    id              = models.IntegerField(primary_key=True, unique=True, null=False)
    is_given        = models.BooleanField(default=False)
    class Meta:
        ordering = ("id", "is_given")
    def __str__(self):
        if self.id == -1 or self.id == 0 :
            return " "
        if self.is_given:
            return f"{self.id} GIVEN"
        else:
            return f"{self.id}"

class GuestEntry(models.Model):
    guest_first_name = models.CharField(max_length=100, blank=False)
    guest_last_name = models.CharField(max_length=100, null=True, blank=True)
    company         = models.CharField(max_length=100, null=True)
    enter_datetime  = models.DateTimeField(blank=False)
    exit_datetime   = models.DateTimeField(null=True, blank=True)
    keeper_full_name= models.CharField(max_length=100, null=True, blank=True)
    notes           = models.CharField(max_length=1000, null=True, blank=True)
    card            = models.ForeignKey(Card, null=True, on_delete=models.DO_NOTHING)
    
    
    class Meta:
        ordering = ("enter_datetime",)
    def __str__(self):
        return f"{self.guest_first_name} {self.guest_last_name} | {self.company} | {self.enter_datetime.strftime('%Y-%m-%d %H:%M')}"
