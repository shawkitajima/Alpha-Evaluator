from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import date


#Company model, the one side on our relation 
class Company(models.Model):
    name = models.CharField(max_length=100)
    ticker = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name



class Performance(models.Model):
    buy = models.DateField()
    sell = models.DateField()
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

   


