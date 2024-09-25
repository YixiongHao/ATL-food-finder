# urls.py
from django.urls import path
from .views import add_favorite, user_favorites

urlpatterns = [
    path('addFavorite/', add_favorite, name='add_favorite'),
    path('favorites/', user_favorites, name='favorites'),
]
