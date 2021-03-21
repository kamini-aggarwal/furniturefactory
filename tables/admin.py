from django.contrib import admin

# Register your models here.

from .models import Table, Feet, Leg

admin.site.register(Table)
admin.site.register(Feet)
admin.site.register(Leg)
