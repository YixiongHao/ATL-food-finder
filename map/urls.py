from django.urls import path
from . import views

urlpatterns = [
    path("map/", views.sign_in, name="map")
]