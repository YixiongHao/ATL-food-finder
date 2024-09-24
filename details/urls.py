from django.urls import path
from . import views

urlpatterns = [
    path('save-restaurants/', views.SaveRestaurantsView.as_view(), name='save_restaurants'), #for creating restaurant database
    path('details/<str:place_id>/', views.restaurant_detail, name='details'),   # for generating restaurant details page
]