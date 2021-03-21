from django.test import TestCase, Client
from tables.models import Table, Leg, Feet
from django.db import IntegrityError, transaction
from django.core.exceptions import ValidationError

# Create your tests here.

client = Client()

class TableTest(TestCase):
    def test_create(self):
        Table(table_name="First Table").save()
        assert Table.objects.count() == 1

    def test_list(self):
        Table(table_name="First Table").save()
        Table(table_name="Second Table").save()
        assert Table.objects.count() == 2

    def test_detail(self):
        Table(table_name="First Table").save()
        Table(table_name="Second Table").save()
        Table(table_name="Third Table").save()
        assert Table.objects.get(pk=1).table_name == "First Table"

    def test_update(self):
        table1 = Table(table_name="First Table")
        table1.save()
        assert Table.objects.get(pk=1).table_name == "First Table"
        table1.table_name = "First Updated Table"
        table1.save()
        self.assertEqual(Table.objects.get(pk=1).table_name, "First Updated Table")

    def test_update_partial(self):
        self.test_update()

    def test_delete(self):
        table1 = Table(table_name="First Table")
        table1.save()
        table1.delete()
        self.assertEqual(Table.objects.count(), 0)

class LegTest(TestCase):
    def test_create(self):
        table1 = Table(table_name="First Table")
        table1.save()
        leg1 = Leg(table_id=table1)
        leg1.save()
        self.assertEqual(Leg.objects.count(), 1)
        self.assertEqual(Leg.objects.get(pk=1).table_id, table1)

    def test_list(self):
        table1 = Table(table_name="First Table")
        table1.save()
        table2 = Table(table_name="Second Table")
        table2.save()
        leg1 = Leg(table_id=table1)
        leg1.save()
        leg2 = Leg(table_id=table2)
        leg2.save()
        self.assertEqual(Leg.objects.count(), 2)

    def test_detail(self):
        table1 = Table(table_name="First Table")
        table1.save()
        leg1 = Leg(table_id=table1)
        leg1.save()
        self.assertEqual(Leg.objects.get(pk=1).table_id, table1)

    def test_update(self):
        table1 = Table(table_name="First Table")
        table1.save()
        table2 = Table(table_name="Second Table")
        table2.save()
        leg1 = Leg(table_id=table1)
        leg1.save()
        self.assertEqual(Leg.objects.get(pk=1).table_id, table1)
        leg1.table_id = table2
        leg1.save()
        self.assertEqual(Leg.objects.get(pk=1).table_id, table2)

    def test_delete(self):
        table1 = Table(table_name="First Table")
        table1.save()
        leg1 = Leg(table_id=table1)
        leg1.save()
        leg1.delete()
        self.assertEqual(Leg.objects.count(), 0)

class FeetTest(TestCase):
    def test_create_circle(self):
        table1 = Table(table_name="First Table")
        table1.save()
        leg1 = Leg(table_id=table1)
        leg1.save()
        foot1 = Feet(radius=1)
        foot1.save()
        foot1.leg.set([leg1])
        foot1.save()
        self.assertEqual(Feet.objects.count(), 1)

    def test_create_rectangle(self):
        table1 = Table(table_name="First Table")
        table1.save()
        leg1 = Leg(table_id=table1)
        leg1.save()
        foot1 = Feet(length=1.7, width=2)
        foot1.save()
        foot1.leg.set([leg1])
        foot1.save()
        self.assertEqual(Feet.objects.count(), 1)

    def test_invalid_data(self):
        table1 = Table(table_name="First Table")
        table1.save()
        leg1 = Leg(table_id=table1)
        leg1.save()
        try:
            with transaction.atomic():
                foot1 = Feet(radius=6, length=1.7, width=2)
                foot1.save()
        except Exception as exception:
            assert "ValidationError" in str(exception)

        try:
            with transaction.atomic():
                foot1 = Feet(length=1.7)
                foot1.save()
        except Exception as exception:
            assert "ValidationError" in str(exception)

        try:
            with transaction.atomic():
                foot1 = Feet(width=1)
                foot1.save()
        except Exception as exception:
            assert "ValidationError" in str(exception)

    def test_list(self):
        self.test_create_circle()

    def test_detail(self):
        table1 = Table(table_name="First Table")
        table1.save()
        table2 = Table(table_name="Second Table")
        table2.save()
        leg1 = Leg(table_id=table1)
        leg1.save()
        leg2 = Leg(table_id=table2)
        leg2.save()
        foot1 = Feet(length=70, width=20)
        foot1.save()
        foot1.leg.set([leg1, leg2])
        foot1.save()
        self.assertEqual(Feet.objects.get(foot_id=1).width, 20)

    def test_update(self):
        table1 = Table(table_name="First Table")
        table1.save()
        leg1 = Leg(table_id=table1)
        leg1.save()
        foot1 = Feet(length=100, width=2)
        foot1.save()
        foot1.leg.set([leg1])
        foot1.save()
        self.assertEqual(Feet.objects.count(), 1)
        self.assertEqual(Feet.objects.get(foot_id=1).length, 100)

        foot1.length = 200
        foot1.save()
        self.assertEqual(Feet.objects.get(foot_id=1).length, 200)

    def test_delete(self):
        table1 = Table(table_name="First Table")
        table1.save()
        leg1 = Leg(table_id=table1)
        leg1.save()
        foot1 = Feet(length=1.7, width=2)
        foot1.save()
        foot1.leg.set([leg1])
        foot1.save()
        self.assertEqual(Feet.objects.count(), 1)
        foot1.delete()
        self.assertEqual(Feet.objects.count(), 0)
