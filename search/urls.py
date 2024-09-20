from django.urls import path
from . import views

urlpatterns = [
    path("", views.search_nearby_restaurants, name='search'),
]