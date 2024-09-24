from django.db import models
from django.contrib.auth.models import User

from details.models import Restaurant


# Create your models here.


class Favorite(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField()
    distance = models.FloatField()
    cuisine = models.CharField(max_length=120)
    rating = models.FloatField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    place_id = models.CharField(max_length=255, unique=True)

    class Meta:
        db_table = 'favorite'
        ordering = ['title']

    def __str__(self):
        return self.title

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.user.username