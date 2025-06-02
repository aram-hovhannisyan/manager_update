from django.db import models

# Create your models here.

class Storage_Element(models.Model):
    count = models.IntegerField(default=0)
    element_name = models.CharField(max_length=255)
    is_available = models.BooleanField(default=True)
    supplier_id = models.IntegerField()
