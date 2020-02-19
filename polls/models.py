import datetime
from django.db import models
from django.utils import timezone

# Create your models here.


class Product(models.Model):                            #Creates the fields for table Product
    type = models.CharField(max_length=200)
    brand = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    price = models.FloatField(max_length=15)
    site = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published', default="2019-1-1 00:00")

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

    def __str__(self):
        return str(f"{self.type}, {self.brand}, {self.name}, {self.price}, {self.site}")
