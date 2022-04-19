from urllib import response
from django.test import TestCase, Client, tag
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User

from .models import GuestEntry, Card

# DATABASE TESTS
class CardTestCase(TestCase):
    def setUp(self):
        card_object = {
        "id": 1,
        "is_given": True 
        }
        Card.objects.create(**card_object)

    def test_card_creation(self):
        card = Card.objects.get(id = 1)
        self.assertEqual(card.is_given, True)

class GuestEntryTestCase(TestCase):

    def setUp(self):
        card_object = {
            "id": 1,
            "is_given": True 
        }
        Card.objects.create(**card_object)
        card = Card.objects.get(id = 1)
        guest_entry = {
            "guest_first_name": "Szymon",
            "guest_last_name": "Sposób",
            "keeper_full_name": "Arkadiusz Szydlik",
            "notes": "Testowe notatki",
            "card": card
        }   
        GuestEntry.objects.create(**guest_entry)

    def test_guest_entry_creation(self):
        guest_entry = GuestEntry.objects.get(guest_first_name="Szymon")
        self.assertEqual(guest_entry.keeper_full_name, "Arkadiusz Szydlik")

# API TESTS        
class LoginTestCase(APITestCase):
    def setUp(self):
        user = User.objects.create(username='testuser')
        user.set_password('qazwsx')
        user.save()
        self.client = Client()

        self.logged_in = self.client.login(username='testuser', password='qazwsx')
        self.not_logged_in1 = self.client.login(username='testuser', password='qaz')
        self.not_logged_in2 = self.client.login(username='asdf', password='qazwsx')

    def test_user_is_logged(self):
        self.assertTrue(self.logged_in)
    
    def test_user_is_not_logged(self):
        self.assertFalse(self.not_logged_in1)
        self.assertFalse(self.not_logged_in2)


class GuestEntryTestCaseAPI(APITestCase):
    def setUp(self):
        self.client = APIClient()
        user = User.objects.create(username='testuser')
        user.set_password('qazwsx')
        user.save()
        self.logged_in = self.client.login(username='testuser', password='qazwsx')

        self.card_object = {
            "id": 1,
            "is_given": False 
        }
        self.card_object10 = {
            "id": 10,
            "is_given": True 
        }
        Card.objects.create(**self.card_object)
        Card.objects.create(**self.card_object10)

        self.data = {
            "guest_first_name": "Jan",
            "guest_last_name": "Kowalski",
            "keeper_full_name": "Adam Sposób",
            "notes": "Testowe notatki",
            "company": "VIGO",
            "card": 1
        }
        self.non_card_data = {
            "guest_first_name": "Jan",
            "guest_last_name": "Kowalski",
            "keeper_full_name": "Adam Sposób",
            "notes": "Testowe notatki",
            "company": "VIGO",
        }
        self.card_data = {
            # "guest_first_name": "Jan",
            # "guest_last_name": "Kowalski",
            # "keeper_full_name": "Adam Sposób",
            # "notes": "Testowe notatki",
            # "company": "VIGO",
            
            "card":1
        }
        self.bad_card_data = [
        {
            "guest_first_name": "Jan",
            "guest_last_name": "Kowalski",
            "keeper_full_name": "Adam Sposób",
            "notes": "Testowe notatki",
            "company": "VIGO",   
        }]

        self.id_data = {
            "guest_first_name": "Jan",
            "guest_last_name": "Kowalski",
            "keeper_full_name": "Adam Sposób",
            "notes": "Testowe notatki",
            "card": 1
        }

        self.put_data = [{
            "guest_first_name": "Jan",
            "guest_last_name": "Kowalski",
            "keeper_full_name": "Adam Sposób",
            "notes": "Gość okazał się bardzo gburowaty i szorstki w obyciu.",
            "card": 1
        },
        {
            "guest_first_name": "Jan",
            "guest_last_name": "Kowalski",
            "keeper_full_name": "Adam Sposób",
            "notes": "Gość okazał się bardzo gburowaty i szorstki w obyciu.",
            "card": 1
        }]

        self.bad_put_data = [
        
        {
            "guest_first_name": "Jan",
            "guest_last_name": "Kowalski",
            "keeper_full_name": "Adam Sposób",
            "notes": "Gość okazał się bardzo gburowaty i szorstki w obyciu.",
            "card": 10 #occupied card number
        }
        ]
        

        self.bad_data = [
        {
            "guest_first_name": "Jan",
            "guest_last_name": "Kowalski",
            "keeper_full_name": "Arkadiusz Szydlik",
            "notes": "Testowe notatki",
            "card": 5
        },
        {
            "guest_first_name": "Jan",
            "guest_last_name": "Kowalski",
            "keeper_full_name": "Arkadiusz Szydlik",
            "notes": "Testowe notatki",
            "card": 'asdfsadf'
        },
        {
            "keeper_full_name": "Arkadiusz Szydlik",
            "notes": "Testowe notatki",
            "card": 5
        },
        {
            "guest_first_name": "Jan II",
            "guest_last_name": "Kowalski",
            "keeper_full_name": "Adam Sposób II",
            "notes": "Testowe notatki",
            "card": 10
        },
        ]

    def test_creation(self):
        response = self.client.post("/api/guest_entries", self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        for data in self.bad_data:
            response = self.client.post("/api/guest_entries", data)
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_getting(self):
        self.client.post("/api/guest_entries", self.data)
        response = self.client.get("/api/guest_entries/1/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get("/api/guest_entries/2/")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.get("/api/guest_entries/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_putting(self):
        self.client.post("/api/guest_entries", self.data)
        for data in self.put_data:
            response = self.client.put("/api/guest_entries/1/", data)
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        for data in self.bad_put_data:
            response = self.client.put("/api/guest_entries/1/", data)
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_deleting(self):
        self.client.post("/api/guest_entries", self.data)
        response = self.client.delete("/api/guest_entries/1/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @tag('wip')
    def test_card_giving(self):
        self.client.post("/api/guest_entries", self.non_card_data)
        response = self.client.put("/api/guest_entries/1/give_card", self.card_data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        entry = GuestEntry.objects.get(pk=1)
        card = Card.objects.get(pk=1)
        self.assertEqual(entry.card, card)

        # for data in self.bad_card_data:
        #     response = self.client.put("/api/guest_entries/1/give_card", self.data)
        #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class CardTestCaseAPI(APITestCase):
    
    def setUp(self):
        self.client = APIClient()
        user = User.objects.create(username='testuser')
        user.set_password('qazwsx')
        user.save()
        self.logged_in = self.client.login(username='testuser', password='qazwsx')
        self.good_data = [
            {
                'id': 1,
                'is_given': 'False'
            },
            {
                'id': 10,
                'is_given': 'True'
            }
        ]
        self.bad_data = [
            {
                'id': 'asdf',
                'is_given': 'False'
            },
            {
                'is_given': 'True'
            },
            {
                'id': 6,
                'is_given': 'asdf'
            },
        ]
    def test_creation(self):
        for data in self.good_data:
            response = self.client.post('/api/cards', data)
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_getting(self):
        self.client.post('/api/cards', self.good_data[0])
        response = self.client.get('/api/cards/1/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    
    def test_putting(self):
        self.client.post('/api/cards', self.good_data[0])
        response = self.client.put('/api/cards/1/', self.good_data[1])
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        for data in self.bad_data:
            response = self.client.put('/api/cards/1/', data)
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    
    def test_deleting(self):
        self.client.post('/api/cards', self.good_data[0])
        response = self.client.delete('/api/cards/1/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
