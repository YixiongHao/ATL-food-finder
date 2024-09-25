# models.py
from django.db import models
from django.contrib.auth.models import User

class Restaurant(models.Model):
    name = models.CharField(max_length=255)
    place_id = models.CharField(max_length=255)  # Google Places ID
    # Other fields like address, rating, etc.

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    place_id = models.CharField(max_length=255)
    name = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.user.username} - {self.name} - {self.place_id}'
