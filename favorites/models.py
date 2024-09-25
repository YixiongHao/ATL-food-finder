from django.db import models
from django.contrib.auth.models import User
from details.models import Restaurant

class Favorite(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='favorites')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    title = models.CharField(max_length=120)
    description = models.TextField()
    distance = models.FloatField()
    cuisine = models.CharField(max_length=120)
    rating = models.FloatField()
    place_id = models.CharField(max_length=255, unique=True)

    class Meta:
        db_table = 'favorite'
        ordering = ['title']

    def __str__(self):
        return self.title

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username
