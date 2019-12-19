from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import date
# Create your models here.



#Company model, the one side on our relation 
class Company(models.Model):
    name = models.CharField(max_length=100)
    ticker = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# Performance model, the many side on our relation
# References Company(fk)
class Performance(models.Model):
    date = models.DateField()
    price = models.IntegerField()

    company = models.ForeignKey(Company, on_delete=models.CASCADE)