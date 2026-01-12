import requests


def get_books(query):
    url = "https://www.googleapis.com/books/v1/volumes"
    params = {'q': query, 'maxResults': 5}
    try:
        response = requests.get(url, params=params)
        data = response.json()
        books = []
        for item in data.get('items', []):
            info = item.get('volumeInfo', {})
            book = {
                'title': info.get('title', ''),
                'author': ', '.join(info.get('authors', [])),
                'pages': info.get('pageCount', 0),
                'description': info.get('description', ''),
            }
            books.append(book)
        return books
    except:
        return []