from django.shortcuts import render, redirect, get_object_or_404
from .models import Book, Reading, Genre
from .services import get_all_books
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .utils import get_or_create_genres, update_user_genre_preferences, calculate_user_genre_stats
from django.db import models


def home(request):
    if request.user.is_authenticated:
        books = Book.objects.filter(user=request.user).order_by('-created')
        paginator = Paginator(books, 10)
        page = request.GET.get('page')
        try:
            books_page = paginator.page(page)
        except PageNotAnInteger:
            books_page = paginator.page(1)
        except EmptyPage:
            books_page = paginator.page(paginator.num_pages)
    else:
        books_page = None
    return render(request, 'home.html', {'books': books_page})


@login_required
def add_book(request):
    if request.method == 'POST':
        title = request.POST['title']
        author = request.POST['author']
        try:
            pages = int(request.POST.get('pages', 0))
        except (ValueError, TypeError):
            pages = 0
        description = request.POST.get('description', '')
        genre_names = request.POST.getlist('genres')
        print(f"Добавляем книгу: {title}, автор: {author}, страниц: {pages}, жанры: {genre_names}")
        book = Book.objects.create(
            title=title,
            author=author,
            pages=pages,
            description=description,
            user=request.user
        )
        if genre_names:
            genres = get_or_create_genres(genre_names)
            book.genres.set(genres)
            book.save()
            update_user_genre_preferences(request.user, book, added=True)
            print(f"Книга добавлена с жанрами: {[g.name for g in genres]}")
        else:
            print("Книга добавлена без жанров")
        return redirect('home')
    all_genres = Genre.objects.all()
    return render(request, 'add_book.html', {'all_genres': all_genres})

@login_required
def delete_book(request, book_id):
    book = get_object_or_404(Book, id=book_id, user=request.user)
    update_user_genre_preferences(request.user, book, added=False)
    book.delete()
    return redirect('home')

def search_books(request):
    query = request.GET.get('q', '')
    books = []
    total_results = 0
    current_page = 1
    total_pages = 1
    if query:
        try:
            current_page = int(request.GET.get('page', 1))
        except ValueError:
            current_page = 1
        session_key = f'search_results_{query}'
        if session_key in request.session:
            all_books = request.session[session_key]
            total_results = len(all_books)
            print(f"Используем кэшированные результаты для '{query}': {total_results} книг")
        else:
            print(f"Делаем новый запрос для '{query}'")
            all_books = get_all_books(query)
            total_results = len(all_books)
            request.session[session_key] = all_books
            request.session.set_expiry(600)
        paginator = Paginator(all_books, 10)
        if current_page > paginator.num_pages:
            current_page = paginator.num_pages
        try:
            books_page = paginator.page(current_page)
            books = books_page.object_list
        except:
            books = []
            current_page = 1
        total_pages = paginator.num_pages
        print(f"Страница {current_page} из {total_pages}, книг на странице: {len(books)}")
    has_previous = current_page > 1
    has_next = current_page < total_pages
    return render(request, 'search.html', {
        'books': books,
        'query': query,
        'total_results': total_results,
        'current_page': current_page,
        'total_pages': total_pages,
        'has_previous': has_previous,
        'has_next': has_next,
        'next_page': current_page + 1,
        'previous_page': current_page - 1,
    })

def book_detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    progress = None
    if request.user.is_authenticated and request.user == book.user:
        try:
            progress = Reading.objects.get(book=book)
        except Reading.DoesNotExist:
            pass
    return render(request, 'book_detail.html', {'book': book, 'progress': progress})

@login_required
def update_reading(request, book_id):
    if request.method == 'POST':
        book = get_object_or_404(Book, id=book_id, user=request.user)
        status = request.POST['status']
        rating = request.POST.get('rating', 0) or 0
        reading, created = Reading.objects.get_or_create(
            book=book,
            defaults={'user': request.user, 'status': status, 'rating': rating}
        )
        if not created:
            reading.status = status
            reading.rating = rating
            reading.save()
        return redirect('book_detail', book_id=book_id)

@login_required
def genre_preferences(request):
    stats = calculate_user_genre_stats(request.user)
    total_books = Book.objects.filter(user=request.user).count()
    total_pages = Book.objects.filter(user=request.user).aggregate(models.Sum('pages'))['pages__sum'] or 0
    top_genres = stats[:5] if len(stats) > 5 else stats
    return render(request, 'genres.html', {
        'stats': stats,
        'total_books': total_books,
        'total_pages': total_pages,
        'top_genres': top_genres,
    })

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
    return render(request, 'login.html')

def user_logout(request):
    logout(request)
    return redirect('home')