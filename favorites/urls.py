# urls.py
from django.urls import path
from .views import add_favorite, remove_favorite, user_favorites, get_favorites

urlpatterns = [
    path('addFavorite/', add_favorite, name='add_favorite'),
    path('removeFavorite/', remove_favorite, name='remove_favorite'),
    path('favorites/', user_favorites, name='favorites'),
    path('get_favorites/', get_favorites, name='get_favorites'),
]
