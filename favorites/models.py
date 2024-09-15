from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class Favorite(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField()
    distance = models.FloatField()
    cuisine = models.CharField(max_length=120)
    rating = models.FloatField()
    post_id = models.BigAutoField(primary_key=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'favorite'
        ordering = ['title']

    def __str__(self):
        return self.title
