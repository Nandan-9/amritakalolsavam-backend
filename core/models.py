from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    HOUSE_CHOICE = [
        ('amritamayi','AMRITAMAYI'),
        ('anandamayi','ANANDAMAYI'),
        ('chinmati','CHINMAYI'),
        ('jyothirmati','JYOTHIRMAYI')
    ]
    roll_number = models.CharField(max_length=200,unique=True,null=False)
    house = models.CharField(max_length=200,choices=HOUSE_CHOICE)

    def __str__(self):
        return self.roll_number
