from django.test import TestCase, Client
from django.db import IntegrityError, transaction
from django.core.exceptions import ValidationError

# Create your tests here.

client = Client()

class TableTestAPI(TestCase):

    def test_create_api(self):
        response = client.post('/table/', {"table_name": "First Table"})
        self.assertEqual(response.status_code, 201)

        response = client.post('/table/', {"table_name": "First Table"})
        self.assertEqual(response.status_code, 400)

    def test_list_api(self):
        client.post('/table/', {"table_name": "First Table"})
        client.post('/table/', {"table_name": "Second Table"})

        response = client.get('/table/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 2)

    def test_detail_api(self):
        client.post('/table/', {"table_name": "First Table"})

        response = client.get('/table/1/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["table_name"], "First Table")

    def test_update_api(self):
        client.post('/table/', {"table_name": "First Table"})
        client.post('/table/', {"table_name": "Second Table"})

        response = client.put('/table/1/',
                              data='{"table_name": "First Updated Table"}',
                              content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["table_name"], "First Updated Table")

        response = client.put('/table/1/',
                              data='{"table_name": "Second Table"}',
                              content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_delete_api(self):
        client.post('/table/', {"table_name": "First Table"})

        response = client.delete('/table/1/')
        self.assertEqual(response.status_code, 204)

        response = client.delete('/table/2/')
        self.assertEqual(response.status_code, 404)

class LegTestAPI(TestCase):

    def test_create_api(self):
        client.post('/table/', {"table_name": "First Table"})
        response = client.post('/leg/', {"table_id": "1"})
        self.assertEqual(response.status_code, 201)

    def test_list_api(self):
        client.post('/table/', {"table_name": "First Table"})
        client.post('/leg/', {"table_id": "1"})
        client.post('/leg/', {"table_id": "1"})
        response = client.get('/leg/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 2)

    def test_detail_api(self):
        client.post('/table/', {"table_name": "First Table"})
        client.post('/leg/', {"table_id": "1"})
        response = client.get('/leg/1/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["table_id"], 1)

    def test_update_api(self):
        client.post('/table/', {"table_name": "First Table"})
        client.post('/table/', {"table_name": "Second Table"})
        client.post('/leg/', {"table_id": "1"})

        response = client.get('/leg/1/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["table_id"], 1)

        response = client.put('/leg/1/',
                              data='{"table_id": "2"}',
                              content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["table_id"], 2)

        response = client.put('/leg/1/',
                              data='{"table_id": "3"}',
                              content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_delete_api(self):
        client.post('/table/', {"table_name": "First Table"})
        client.post('/leg/', {"table_id": "1"})

        response = client.delete('/leg/1/')
        self.assertEqual(response.status_code, 204)

        response = client.delete('/leg/2/')
        self.assertEqual(response.status_code, 404)


class FeetTestAPI(TestCase):
    def test_create_circle_api(self):
        client.post('/table/', {"table_name": "First Table"})
        client.post('/leg/', {"table_id": "1"})
        response = client.post('/feet/', {"leg": [1], "radius": 10})
        self.assertEqual(response.status_code, 201)

    def test_create_rectangle_api(self):
        client.post('/table/', {"table_name": "First Table"})
        client.post('/leg/', {"table_id": "1"})
        client.post('/leg/', {"table_id": "1"})
        response = client.post(
            '/feet/', {"leg": [1, 2], "length": 10, "width": 20})
        self.assertEqual(response.status_code, 201)

    def test_invalid_data_api(self):
        client.post('/table/', {"table_name": "First Table"})
        client.post('/leg/', {"table_id": "1"})
        client.post('/leg/', {"table_id": "1"})

        try:
            with transaction.atomic():
                client.post('/feet/', {"leg": [1, 2], "radius": 1, "length": 10, "width": 20})
        except Exception as exception:
            assert "ValidationError" in str(exception)

        try:
            with transaction.atomic():
                client.post('/feet/', {"leg": [1, 2], "length": 10})
        except Exception as exception:
            assert "ValidationError" in str(exception)

        try:
            with transaction.atomic():
                client.post('/feet/', {"leg": [1, 2], "Width": 20})
        except Exception as exception:
            assert "ValidationError" in str(exception)

    def test_list_api(self):
        client.post('/table/', {"table_name": "First Table"})
        client.post('/leg/', {"table_id": "1"})
        client.post('/leg/', {"table_id": "1"})
        client.post('/leg/', {"table_id": "1"})
        response = client.post('/feet/', {"leg": [1, 2, 3], "radius": 1.0})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["foot_id"], 1)

    def test_update_api(self):
        client.post('/table/', {"table_name": "First Table"})
        client.post('/leg/', {"table_id": "1"})
        client.post('/leg/', {"table_id": "1"})
        response = client.post('/feet/', {"leg": [1], "length": 10, "width": 20})
        self.assertEqual(response.json()["length"], 10)

        response = client.put('/feet/1/',
                              data='{"leg": [1, 2], "length": 100}',
                              content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["length"], 100)
        self.assertEqual(response.json()["leg"], [1, 2])

    def test_delete_api(self):
        client.post('/table/', {"table_name": "First Table"})
        client.post('/leg/', {"table_id": "1"})
        client.post('/feet/', {"leg": [1], "length": 1, "width": 2})
        response = client.delete('/feet/1/')
        self.assertEqual(response.status_code, 204)

        response = client.delete('/feet/2/')
        self.assertEqual(response.status_code, 404)
