import json
import hashlib
from flask import Flask, request, Response, session, redirect, url_for
from dicttoxml import dicttoxml
from googletrans import Translator, LANGUAGES
from db import DB

app = Flask(__name__)
app.secret_key = b'\x08\xc3\x10\x17\nnl\xd3\xa8O\xf1h\x04\x8d\xd8\x1d'
db = DB()


def to_json(data):
    return json.dumps(data) + "\n"


def to_xml(data):
    return dicttoxml(data, attr_type=False)


def resp(code, data, out_format='json'):
    if out_format == 'xml':
        return Response(status=code, mimetype="application/xml", response=to_xml(data))
    else:
        return Response(status=code, mimetype="application/json", response=to_json(data))


def collect_scions(obj):
    out = [obj]
    data = db.execute(f'SELECT * FROM objects WHERE parent={obj[0]}')
    for item in data:
        scions = collect_scions(item)
        if scions:
            for scion in scions:
                if scion:
                    out.append(scion)
    return out


def tuple_to_dict(tuple_object_list):
    new_dict_object_list = list()
    for tuple_object in tuple_object_list:
        new_dict_object_list.append({
            'id': tuple_object[0],
            'name': tuple_object[1],
            'parent': tuple_object[2],
            'type': tuple_object[3],
            'value': tuple_object[4]
        })
    return new_dict_object_list


# Реализовать обработку ошибок
@app.errorhandler(400)
def page_not_found(e):
    return resp(400, [])


@app.errorhandler(404)
def page_not_found(e):
    return resp(404, [])


@app.errorhandler(500)
def page_not_found(e):
    return resp(500, [])

# Необходимо реализовать REST-сервис, принимающий запрос GET /object/<id>/
@app.route('/objects/', methods=['GET'])
def get_themes():
    # Отображение объектов согласно уровню прав доступа текущего пользователя
    if 'username' not in session:
        return resp(404, [])
    # Если id=0 или не задан - должны вывестись все объекты БД
    if 'id' not in request.args or request.args.get('id') == '0':
        # filter=name - фильтрация по имени объекта (нестрогое соответствие)
        if 'filter' in request.args:
            data = db.execute(f"SELECT * FROM objects WHERE name LIKE '%{request.args.get('filter')}%'")
        else:
            data = db.execute("SELECT * FROM objects")
        # Если при выполнении запроса возникла иная ошибка - HTTP 500
        if data != 'error':
            # Если объекта не существует - должна вернуться ошибка HTTP 404
            if not data:
                return resp(404, [])
        else:
            return resp(500, [])
    else:
        # Если id задан и не цифра - должна вернуться ошибка HTTP 400, с описанием проблемы
        if request.args.get('id').isdigit():
            data = db.execute(f"SELECT * FROM objects WHERE id = {int(request.args.get('id'))}")
            if data != 'error':
                if not data:
                    return resp(404, [])
            else:
                return resp(500, [])
            # Если указанный объект имеет потомков - должны быть выведены все объекты-потомки указанного объекта,
            # а также сам объект
            data = collect_scions(data[0])
        else:
            return resp(400, ['error: Field id is not a number'])

    data = tuple_to_dict(data)

    # Реализовать локализацию объектов по имени. Добавить новый GET-параметр lng, в зависимости от значения которого
    # выводить имя объекта на том или ином языке. TODO Параметр также будет влиять на работу filter
    if 'lng' in request.args and data:
        if request.args.get('lng') in LANGUAGES:
            google = Translator()
            for i in range(len(data)):
                data[i]["name"] = google.translate(data[i].get("name"), scr='en', dest=request.args.get('lng')).text

    # Реализовать механизм кэширования ответов
    md5 = hashlib.md5(str(data).encode('utf-8')).hexdigest()
    data.append({'md5': md5})

    # format=json/xml - формат выдаваемых данных (если не указан - json)
    return resp(200, data, request.args.get('format'))


# Реализовать механизм прав доступа
@app.route('/')
def index():
    if 'username' in session:
        return f'Вы авторизированы как {session["username"]}'
    return 'Авторизация не пройдена'


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('index'))
    return '''
        <form method="post">
            <p><input type=text name=username>
            <p><input type=submit value=Войти>
        </form>
    '''


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.debug = True
    app.run()
