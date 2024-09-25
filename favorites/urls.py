from django.urls import path
from .views import favorite_restaurant
from .views import user_favorites

urlpatterns = [
    path('favorite-restaurant/', favorite_restaurant, name='favorite_restaurant'),
    path('favorites/', user_favorites, name='user_favorites'),
]