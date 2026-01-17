import requests


def get_all_books(query):
    url = "https://www.googleapis.com/books/v1/volumes"
    all_books = []
    params = {
        'q': f'{query}',
        'maxResults': 40,
        'orderBy': 'relevance',
        'langRestrict': 'ru',
        'printType': 'books'
    }
    try:
        start_index = 0
        while len(all_books) < 100:
            params['startIndex'] = start_index
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            items = data.get('items', [])
            if not items:
                break
            for item in items:
                info = item.get('volumeInfo', {})
                if info.get('title') and info.get('authors'):
                    book = {
                        'title': info.get('title', ''),
                        'author': ', '.join(info.get('authors', [])),
                        'pages': info.get('pageCount', 0),
                        'description': info.get('description', 'Описание отсутствует'),
                        'id': item.get('id', ''),
                    }
                    all_books.append(book)
            start_index += len(items)
            if len(items) < params['maxResults']:
                break
        print(f"Получено {len(all_books)} книг по запросу '{query}'")
        return all_books
    except Exception as e:
        print(f"Ошибка при запросе к API: {e}")
        return []