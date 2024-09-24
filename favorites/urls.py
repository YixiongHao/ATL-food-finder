from django.urls import path
from .views import favorite_restaurant

urlpatterns = [
    path('favorite-restaurant/', favorite_restaurant, name='favorite_restaurant'),
]