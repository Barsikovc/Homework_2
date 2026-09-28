"""URL-маршруты приложения books."""
from django.urls import path

from . import views

app_name = 'books'

urlpatterns = [
    path('', views.book_list, name='book_list'),
    path('genres/', views.genre_list, name='genre_list'),
    path('create/', views.book_create, name='book_create'),
    path('<int:pk>/', views.book_detail, name='book_detail'),
]
