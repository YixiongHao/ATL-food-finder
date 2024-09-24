from django.db import models

class Restaurant(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    place_id = models.CharField(max_length=255, unique=True)
    link_name = models.CharField(max_length=255)
    lat = models.DecimalField(max_digits=9, decimal_places=6)
    lng = models.DecimalField(max_digits=9, decimal_places=6)
    is_favorite = models.BooleanField(default=False)

    def __str__(self):
        return self.name

