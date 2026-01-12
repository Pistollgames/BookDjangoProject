from django.shortcuts import render, redirect
from .models import Book, Reading
from .services import get_books


def home(request):
    books = Book.objects.all()
    return render(request, 'home.html', {'books': books})

def add_book(request):
    if request.method == 'POST':
        title = request.POST['title']
        author = request.POST['author']
        pages = request.POST.get('pages', 0)
        Book.objects.create(title=title, author=author, pages=pages)
        return redirect('home')
    return render(request, 'add_book.html')

def search_books(request):
    books = []
    if 'q' in request.GET:
        query = request.GET['q']
        books = get_books(query)
    return render(request, 'search.html', {'books': books, 'query': request.GET.get('q', '')})

def book_detail(request, book_id):
    book = Book.objects.get(id=book_id)
    return render(request, 'book_detail.html', {'book': book})

def update_reading(request, book_id):
    if request.method == 'POST':
        book = Book.objects.get(id=book_id)
        status = request.POST['status']
        rating = request.POST.get('rating', 0)
        reading, created = Reading.objects.get_or_create(book=book)
        reading.status = status
        reading.rating = rating
        reading.save()
        return redirect('book_detail', book_id=book_id)