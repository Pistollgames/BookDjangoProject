from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('add/', views.add_book, name='add_book'),
    path('search/', views.search_books, name='search_books'),
    path('book/<int:book_id>/', views.book_detail, name='book_detail'),
    path('book/<int:book_id>/update/', views.update_reading, name='update_reading'),
    path('book/<int:book_id>/delete/', views.delete_book, name='delete_book'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('genres/', views.genre_preferences, name='genre_preferences'),  # Новый маршрут
]