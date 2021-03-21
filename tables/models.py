from django.db import models

# Create your models here.

from django.db.models import Q
from django.core.exceptions import ValidationError

# Create your models here.

class Table(models.Model):
    table_name = models.CharField(max_length=128, unique=True)

    def __str__(self):
        return self.table_name

    class Meta:
      db_table = "table"

class Leg(models.Model):
    table_id = models.ForeignKey(Table, on_delete=models.CASCADE)

    class Meta:
      db_table = "leg"

class Feet(models.Model):
    foot_id = models.AutoField(primary_key = True)
    width = models.IntegerField(default=None, blank=True, null=True)
    length = models.IntegerField(default=None, blank=True, null=True)
    radius = models.IntegerField(default=None, blank=True, null=True)
    leg = models.ManyToManyField(Leg)

    def clean(self):
        if self.radius and (self.length or self.width):
            raise ValidationError('ValidationError : A foot with a radius must not have length or width')
        if self.length and not self.width:
            raise ValidationError('ValidationError : A foot with a length must also have a width')
        if self.width and not self.length:
            raise ValidationError('ValidationError : A foot with a width must also have a length')

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    class Meta:
      db_table = "feet"
