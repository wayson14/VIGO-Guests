import openpyxl
from pathlib import Path
import datetime
from .serializers import GuestEntrySerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import pytz


class Importer(APIView):

    def get(self, request):
        xlsx_file = Path("api/data.xlsx")
        wb_obj = openpyxl.load_workbook(xlsx_file) 

        # Read the active sheet:
        sheet = wb_obj.active

        i = 2
        for row in sheet.iter_rows(min_row=2, max_row=9982):
            guest_full_name = row[1].value
            if not guest_full_name:
                guest_full_name = "Niewiadoma Bezimienna"
                print("Niewiadoma Bezimienna at "+str(i))
            guest_full_name = guest_full_name.strip()
            if guest_full_name == "":
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
            else: card = -1

            entry_datetime = row[0].value
            if not isinstance(entry_datetime, datetime.datetime):
                entry_datetime = datetime.datetime(1970, 1, 1, 8, 21, 37)
                print("Wrong datetime at "+str(i))
            
            exit_time = row[7].value
            if not isinstance(exit_time, datetime.time): exit_time = datetime.time(18, 21, 37)
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
            if serializer.is_valid():
                serializer.save()
            else: print("Row not valid - "+str(i))
            if(i%100 == 0): print("Passed row "+str(i))
            i += 1
        print("Importing completed!")
        return Response(serializer.data, status=status.HTTP_200_OK)