from django.shortcuts import render

# Create your views here.

from rest_framework import viewsets
from .restapi import TableSerialize, FeetSerialize, LegSerialize
from .models import Table, Feet, Leg

class TableViewSet(viewsets.ModelViewSet):
        queryset = Table.objects.all()
        serializer_class = TableSerialize

class FeetViewSet(viewsets.ModelViewSet):
        queryset = Feet.objects.all()
        serializer_class = FeetSerialize

class LegViewSet(viewsets.ModelViewSet):
        queryset = Leg.objects.all()
        serializer_class = LegSerialize
