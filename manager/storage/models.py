from django.db import models

# Create your models here.

class Storage_Element(models.Model):
    count = models.IntegerField(default=0)
    element_name = models.CharField(max_length=255)
    is_available = models.BooleanField(default=True)
    supplier_id = models.IntegerField(default=0)
    modified_date = models.DateField(null=True)


class Tmp_Elements_Values(models.Model):
    element = models.ForeignKey(Storage_Element, on_delete=models.CASCADE)
    tmp_val = models.IntegerField(default=0)
    date = models.DateField(null=False)


class Non_Working_Days(models.Model):
    day = models.DateField(null=False)
