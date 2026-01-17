from django.db import models
from django.contrib.auth.models import User


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    pages = models.IntegerField(default=0)
    description = models.TextField(blank=True, default='')
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.title

class Reading(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    status_choices = [
        ('want', 'Хочу прочитать'),
        ('reading', 'Читаю'),
        ('done', 'Прочитано'),
    ]
    status = models.CharField(max_length=20, choices=status_choices, default='want')
    rating = models.IntegerField(default=0, choices=[(i, i) for i in range(1, 6)])
    def __str__(self):
        return f"{self.book.title} - {self.status}"

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