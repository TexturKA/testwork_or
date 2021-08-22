import requests


def start():
    url = 'http://localhost:5000/objects/'
    params = [
        {'id': 65},
        {'format': 'json'},
        {'id': 1200},
        {'id': 89, 'format': 'xml'},
        {'id': 'two'},
        {'filter': 'rest'},
        {'id': 358, 'lng': 'ru', 'format': 'xml'}
    ]

    url_login = 'http://localhost:5000/login'
    print('Authorizing...   ', end='')
    session = requests.Session()
    session.post(url_login, {'username': 'Admin'})
    print('Done!\n\n')

    for param in params:
        print(f'Запрос:\n{param}')
        out = session.get(url, params=param)
        print(f'Ответ: {out.status_code};\n{out.text}\n')


if __name__ == '__main__':
    start()
