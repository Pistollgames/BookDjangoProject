from django.db import models
from django.contrib.auth.models import User


class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    pages = models.IntegerField(default=0)
    description = models.TextField(blank=True, default='')
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    genres = models.ManyToManyField(Genre, blank=True)
    def __str__(self):
        return self.title

class Reading(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status_choices = [
        ('want', 'Хочу прочитать'),
        ('reading', 'Читаю'),
        ('done', 'Прочитано'),
    ]
    status = models.CharField(max_length=20, choices=status_choices, default='want')
    rating = models.IntegerField(default=0, choices=[(i, i) for i in range(1, 6)])
    updated = models.DateTimeField(auto_now=True)
    class Meta:
        unique_together = ['book', 'user']
    def __str__(self):
        return f"{self.book.title} - {self.status}"

class UserGenrePreference(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    book_count = models.IntegerField(default=0)
    total_pages = models.IntegerField(default=0)
    average_rating = models.FloatField(default=0)
    last_updated = models.DateTimeField(auto_now=True)
    class Meta:
        unique_together = ['user', 'genre']
    def __str__(self):
        return f"{self.user.username} - {self.genre.name}: {self.book_count} книг"