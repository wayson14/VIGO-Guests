import openpyxl
from pathlib import Path
import datetime
from .models import *
from .serializers import CardSerializer, GuestEntrySerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import pytz
from django.contrib.auth.decorators import user_passes_test

class Importer(APIView):

    # @user_passes_test(lambda u: u.is_superuser)
    def get(self, request):
        cards = Card.objects.all()
        occured = []
        for card in cards:
            if card.id >= -1 and card.id <= 50:
                occured.append(card.id)
                if occured.count(card.id) > 1:
                    return Response("one card occured multiple times inside a range")
        
        i = -2
        for i in range(51):
            if not i in occured:
                card_object = {
                    "id": i,
                    "is_given": False 
                }
                serializer = CardSerializer(data = card_object)
                if serializer.is_valid():
                    serializer.save()
                else:
                    print(f'Adding stopped at {i} card')
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            # return Response("OK")
        
        
        xlsx_file = Path("api/data.xlsx")
        wb_obj = openpyxl.load_workbook(xlsx_file) 

        # Read the active sheet:
        sheet = wb_obj.active
        penalty = 0
        i = 2
        for row in sheet.iter_rows(min_row=2, max_row=20000):
            guest_full_name = row[1].value
            if not guest_full_name:
                penalty += 1
                guest_full_name = "Niewiadoma Bezimienna"
                print("Niewiadoma Bezimienna at "+str(i))
            guest_full_name = guest_full_name.strip()
            if guest_full_name == "":
                penalty +=1
                guest_full_name = "Niewiadoma Bezimienna"
                print("Niewiadoma Bezimienna at "+str(i))
            guest_full_name = guest_full_name.split(" ")
            guest_first_name = guest_full_name[0]
            if len(guest_full_name) < 2:
                guest_full_name.append("")
            guest_last_name = " ".join(guest_full_name[1:])

            company = row[2].value
            keeper_full_name = row[3].value

            card = row[4].value
            if card: card = int(card)
            else: card = None

            entry_datetime = row[0].value
            if not isinstance(entry_datetime, datetime.datetime):
                penalty +=1
                entry_datetime = datetime.datetime(1970, 1, 1, 8, 21, 37)
                print("Wrong datetime at "+str(i))
            
            exit_time = row[7].value
            if not isinstance(exit_time, datetime.time): 
                penalty +=1
                exit_time = datetime.time(18, 21, 37)
            exit_datetime = pytz.timezone('Poland').localize(datetime.datetime.combine(date=entry_datetime.date(), time=exit_time))
            exit_datetime = pytz.timezone('GMT').normalize(exit_datetime)
            exit_datetime.replace(tzinfo=None)

            notes = row[9].value
            data = {
                'guest_first_name': guest_first_name,
                'guest_last_name': guest_last_name,
                'keeper_full_name': keeper_full_name,
                'notes': notes,
                'card': card,
                'company': company,
                'enter_datetime': entry_datetime,
                'exit_datetime': exit_datetime
            }
            
            serializer = GuestEntrySerializer(data = data)
            if serializer.is_valid() and penalty <4:
                serializer.save()
            else: 
                print('==============')
                print(data)
                print('==============')
                print("Row not valid - "+str(i))
                print("ERRORS:", serializer.errors)

            if(i%100 == 0): print(f"{serializer.errors}Passed row "+str(i))
            i += 1
        print("Importing completed!")
        penalty = 0
        return Response(serializer.data, status=status.HTTP_200_OK)