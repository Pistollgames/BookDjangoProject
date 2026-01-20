from .models import Genre, Book, UserGenrePreference, Reading


def update_user_genre_preferences(user, book, added=True):
    pages = int(book.pages) if book.pages else 0
    if added:
        for genre in book.genres.all():
            pref, created = UserGenrePreference.objects.get_or_create(
                user=user,
                genre=genre,
                defaults={
                    'book_count': 1,
                    'total_pages': pages,
                    'average_rating': 0
                }
            )
            if not created:
                pref.book_count += 1
                pref.total_pages += pages
                pref.save()
    else:
        for genre in book.genres.all():
            try:
                pref = UserGenrePreference.objects.get(user=user, genre=genre)
                pref.book_count -= 1
                pref.total_pages -= pages
                if pref.book_count <= 0:
                    pref.delete()
                else:
                    pref.save()
            except UserGenrePreference.DoesNotExist:
                pass

def get_or_create_genres(genre_names):
    genres = []
    for name in genre_names:
        if name and name.strip():  # Пропускаем пустые строки и пробелы
            genre, created = Genre.objects.get_or_create(
                name=name[:100].strip(),  # Ограничиваем длину и убираем пробелы
                defaults={'description': ''}
            )
            genres.append(genre)
    return genres

def calculate_user_genre_stats(user):
    preferences = UserGenrePreference.objects.filter(user=user)
    stats = []
    for pref in preferences:
        from django.db.models import Avg
        avg_rating = Reading.objects.filter(
            user=user,
            book__genres=pref.genre,
            rating__gt=0
        ).aggregate(Avg('rating'))['rating__avg'] or 0
        pref.average_rating = avg_rating
        pref.save()
        total_user_books = Book.objects.filter(user=user).count()
        stats.append({
            'genre': pref.genre,
            'book_count': pref.book_count,
            'total_pages': pref.total_pages,
            'average_rating': round(avg_rating, 1),
            'percentage': round((pref.book_count / total_user_books) * 100, 1)
            if total_user_books > 0 else 0
        })
    return sorted(stats, key=lambda x: x['book_count'], reverse=True)