from flask import Flask, request, make_response
from pytz import timezone
from datetime import datetime
import json

app = Flask(__name__)


"""Для хранения городов создается глобальная переменная LIST_OF_CITIES, 
   в ней хранятся города в виде списка значений полей. Также создана 
   глобальная перемнная AMOUNT_OF_CITIES, в которой хранится количесво городов в файле.
   
"""

LIST_OF_CITIES = []
with open("RU.txt", 'r', encoding='utf-8') as f:
    for raw_line in f:
        LIST_OF_CITIES.append(raw_line.split('\t'))

    AMOUNT_OF_CITIES = len(LIST_OF_CITIES)


def dict_maker(city):
    """
    Данная функция получает на вход переменную city - список полей
    города, и преобразует ее в словарь для работы с объектами в дальнейшем

    :param city:
    :return Dict:
    """

    return {
        'geonameid': int(city[0]),
        'name': city[1],
        'asciiname': city[2],
        'alternatenames': city[3],
        'latitude': float(city[4]),
        'longitude': float(city[5]),
        'feature class': city[6],
        'feature code': city[7],
        'country code': city[8],
        'cc2': city[9],
        'admin1 code': city[10],
        'admin2 code': city[11],
        'admin3 code': city[12],
        'admin4 code': city[13],
        'population': int(city[14]),
        'elevation': city[15],
        'dem': city[16],
        'timezone': city[17],
        'modification date': city[18].split("\n")[0]
    }



def id_searcher(id_name):
    """
    Данная функция принимает id_name - geonameid искомого города.
    С помощью бинарного поиска оптимизирован алгоритм поиска города, так как
    в файле, с которым работает программа много данных.
    Функция возвращает индекс - позиция города в списке LIST_OF_CITIES,
    если город не найден, программа возвращает -1

    :param id_name:
    :return Int:
    """

    first = 0
    last = AMOUNT_OF_CITIES - 1
    index = -1

    while (first <= last) and (index == -1):
        mid = (first + last) // 2
        if int(LIST_OF_CITIES[mid][0]) == id_name:
            index = mid
        else:
            if id_name < int(LIST_OF_CITIES[mid][0]):
                last = mid - 1
            else:
                first = mid + 1

    return index


def name_searcher(ru_name):
    """
     Данная функция принимает ru_name - имя искомого города на русском языке.
    Функция проходит по списку городов и ищет элементы, у которых в графе alternatenames
    присутствует запрашиваемое имя, добавляя этот элемент в список result.
    Далее, если таких городов оказалось несколько, она сортирует их по популяции
    и выбирает город с большим населнием.
    Функция возвращает искомый город в виде словаряс помощью функции dict_maker,
    если города не нашлось, функция отправляет сообщение-исключение.

    :param ru_name:
    :return Dict:
    """

    result_list = []

    for city in LIST_OF_CITIES:
        if ru_name in city[3]:
            result_list.append(city)

    if len(result_list) > 1:
        result_list = sorted(result_list, key=lambda population: int(population[14]))
        return dict_maker(result_list[-1])
    elif len(result_list) == 1:
        return dict_maker(result_list[0])
    else:
        raise Exception(f'There is no {ru_name} city in the file')


def page_maker(page_num, amount):
    """
    Данная функция принимает два параметра: page_num - номер искомой страницы,
    amount - количесво городов на странице.
    Если запрашиваемой страницы не существует, функция отправляет сообщение-исключение.
    Если страница неполная (например, последняя), то функция вернет
    список городов, приведенных к словарю с помошью функции dict_maker
    с меньшим или равным amount количеством объектов.

    :param page_num:
    :param amount:
    :return List of Dicts:
    """

    amount_of_pages = AMOUNT_OF_CITIES // amount
    if AMOUNT_OF_CITIES % amount > 0:
        amount_of_pages += 1

    from_id = amount * (page_num - 1)
    to_id = amount * page_num
    result_list = []

    if amount_of_pages > 0 and to_id <= AMOUNT_OF_CITIES >= from_id:
        for i in range(from_id, to_id):
            result_list.append(dict_maker(LIST_OF_CITIES[i]))
    elif amount_of_pages > 0 and from_id <= AMOUNT_OF_CITIES <= to_id:
        for i in range(from_id, AMOUNT_OF_CITIES):
            result_list.append(dict_maker(LIST_OF_CITIES[i]))
    else:
        raise Exception("GET request is incorrect for this file, something wrong with page_num or amount. Try to use "
                        "another numbers")

    return result_list


def compare_cities(city1, city2, param):
    """
    Данная функця принимает на вход city1, city2 - города-словари, которые
    требуют сравнения по параметру param. В данный момент осуществляется
    сравнение по параметрам: ширина, временная зона.
    Для param = 'latitude', функция сравнивает координатную широту городов
    и возвращает словарь: {'same latitude' = bool, 'on the north' = asciiname}
    Для param = 'timezone', функция сравнивает название временной зоны
    и с помощью библиотеки pytz и локализации времени находит разницу
    во времени между городами, если она сеть.
    Возвращает словарь: {'same timezone': bool, 'difference': str}

    :param city1:
    :param city2:
    :param param:
    :return Dict:
    """

    result = {}
    if param == 'latitude':
        if city1[param] > city2[param]:
            result['same latitude'] = False
            result['on the north'] = city1['asciiname']
        elif city2[param] > city1[param]:
            result['same latitude'] = False
            result['on the north'] = city2['asciiname']
        else:
            result['same latitude'] = True
            result['on the north'] = None

    if param == 'timezone':

        if city1[param] == city2[param]:
            result['same timezone'] = True
            result['difference'] = None
        else:
            now_utc = datetime.utcnow()

            city1_tz = timezone(city1[param])
            city2_tz = timezone(city2[param])

            now_city1 = city1_tz.localize(now_utc)
            now_city2 = city2_tz.localize(now_utc)

            result['same timezone'] = False
            result['difference'] = str(now_city1 - now_city2)

    return result


@app.route('/')
def first_page():
    return make_response({'data': 'this is a blank page :^)'})


@app.route('/info_about_city', methods=['GET'])
def info_about_city():
    """
    Метод принимает идентификатор geonameid и возвращает информацию о городе
    А также обрабатывает ошибки, информацию возвращает в виде Response объекта

    :return Response obj:
    """

    try:
        geonameid = int(request.args.get('geonameid'))
        result_id = id_searcher(geonameid)
        if result_id == -1:
            raise Exception('There is no city with such geonameid')
        result = dict_maker(LIST_OF_CITIES[result_id])
        return make_response(json.dumps(result))

    except ValueError:
        return make_response(json.dumps({'ERROR': 'there is something wrong with the GET request, argument '
                                                  'geonameid=<int> is reqired'}), 401)
    except Exception as e:
        return make_response(json.dumps({'ERROR': str(e)}), 404)


@app.route('/cities_on_page', methods=['GET'])
def cities_on_the_page():
    """
    Метод принимает страницу и количество отображаемых на странице городов и возвращает список городов с их информацией
    А также обрабатывает ошибки, информацию возвращает в виде Response объекта

    :return Response obj:
    """

    try:
        page = int(request.args.get('page'))
        amount = int(request.args.get('amount'))
        result = page_maker(page, amount)
        return json.dumps(result)
    except ValueError:
        return make_response(json.dumps({'ERROR': 'there is something wrong with the GET request, arguments '
                                                  'page=<int> and amount=<int> are required'}), 401)
    except Exception as e:
        return make_response(json.dumps({'ERROR': str(e)}), 404)


@app.route('/info_about_two_cities', methods=['GET'])
def info_about_two_cities():
    """
    Метод принимает названия двух городов (на русском языке)
    и получает информацию о найденных городах, а также дополнительно:
    какой из них расположен севернее и одинаковая ли у них временная зона
    (когда несколько городов имеют одно и то же название, разрешать
    неоднозначность выбирая город с большим населением;
    если население совпадает, брать первый попавшийся)
    А также обрабатывает ошибки, информацию возвращает в виде Response объекта

    :return Response obj:
    """

    try:
        result = []
        city1_name = request.args.get('city1')
        city2_name = request.args.get('city2')

        city1_info = name_searcher(city1_name)
        city2_info = name_searcher(city2_name)
        result.append(city1_info)
        result.append(city2_info)

        result.append(compare_cities(city1_info, city2_info, 'latitude'))
        result.append(compare_cities(city1_info, city2_info, 'timezone'))

        return make_response(json.dumps(result))
    except Exception as e:
        return make_response(json.dumps({'ERROR': str(e)}), 401)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000)
