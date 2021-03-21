from rest_framework import serializers

from .models import Table, Feet, Leg

class TableSerialize(serializers.ModelSerializer):
    class Meta:
        model = Table
        fields = ('__all__')

class FeetSerialize(serializers.ModelSerializer):
    class Meta:
        model = Feet
        fields = ('__all__')

class LegSerialize(serializers.ModelSerializer):
    class Meta:
        model = Leg
        fields = ('__all__')
