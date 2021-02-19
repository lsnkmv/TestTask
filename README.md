## Задание
Реализовать HTTP-сервер для предоставления информации по географическим объектам.
Данные взять из географической базы данных GeoNames, по [ссылке](http://download.geonames.org/export/dump/RU.zip).
Описание формата данных можно найти по [ссылке](http://download.geonames.org/export/dump/readme.txt).
## Описание программы
В данной работе реализован HTTP-сервер для работы с информацией по географическим объектам из базы "GeoNames". Для реализации сервера использовался фреймворк Flask.   Программа предназначена для работы с файлом "RU.txt". Требования: данный файл должен находиться в той же директории, что и программа.  

#### Описание методов, реализованных в программе:  
1. Метод принимает идентификатор <geonameid> и взвращает информацию о городе:  
```sh
    @app.route('/info_about_city', methods=['GET'])  
	def info_about_city()
```
 > Пример GET запроса:
  ```sh
    http://127.0.0.1:8000/info_about_city?geonameid=451750
```
>Данные от сервера:
```
{
    "geonameid": 451750,
    "name": "Zhitovo",
    "asciiname": "Zhitovo",
    "alternatenames": "",
    "latitude": 57.29693,
    "longitude": 34.41848,
    "feature class": "P",
    "feature code": "PPL",
    "country code": "RU",
    "cc2": "",
    "admin1 code": "77",
    "admin2 code": "",
    "admin3 code": "",
    "admin4 code": "",
    "population": 0,
    "elevation": "",
    "dem": "247",
    "timezone": "Europe/Moscow",
    "modification date": "2011-07-09"
}
```
 
2. Метод принимает страницу и количество отображаемых на странице городов и возвращает список городов с их информацией.   
```
@app.route('/cities_on_page', methods=['GET'])
def cities_on_the_page(): 
```
 > Пример GET запроса:
  ```sh
   http://127.0.0.1:8000/cities_on_page?page=6&amount=3
```
>Данные от сервера:
```
[
    {
        "geonameid": 451762,
        "name": "Yeskino",
        "asciiname": "Yeskino",
        "alternatenames": "",
        "latitude": 57.07916,
        "longitude": 34.78913,
        "feature class": "P",
        "feature code": "PPL",
        "country code": "RU",
        "cc2": "",
        "admin1 code": "77",
        "admin2 code": "",
        "admin3 code": "",
        "admin4 code": "",
        "population": 0,
        "elevation": "",
        "dem": "189",
        "timezone": "Europe/Moscow",
        "modification date": "2011-07-09"
    },
    {
        "geonameid": 451763,
        "name": "Yereshkino",
        "asciiname": "Yereshkino",
        "alternatenames": "",
        "latitude": 57.22681,
        "longitude": 34.58422,
        "feature class": "P",
        "feature code": "PPL",
        "country code": "RU",
        "cc2": "",
        "admin1 code": "77",
        "admin2 code": "",
        "admin3 code": "",
        "admin4 code": "",
        "population": 0,
        "elevation": "",
        "dem": "218",
        "timezone": "Europe/Moscow",
        "modification date": "2011-07-09"
    },
    {
        "geonameid": 451764,
        "name": "Yeremeyki",
        "asciiname": "Yeremeyki",
        "alternatenames": "",
        "latitude": 56.81639,
        "longitude": 34.92389,
        "feature class": "P",
        "feature code": "PPL",
        "country code": "RU",
        "cc2": "",
        "admin1 code": "77",
        "admin2 code": "",
        "admin3 code": "",
        "admin4 code": "",
        "population": 0,
        "elevation": "",
        "dem": "160",
        "timezone": "Europe/Moscow",
        "modification date": "1998-05-01"
    }
]
```
3. Метод принимает названия двух городов (на русском языке) и получает информацию о найденных городах, а также дополнительно: какой из них расположен севернее и одинаковая ли у них временная зона (когда несколько городов имеют одно и то же название, разрешать неоднозначность выбирая город с большим населением; если население совпадает, брать первый попавшийся)

```sh
@app.route('/info_about_two_cities', methods=['GET'])
def info_about_two_cities():
```
 > Пример GET запроса:
  ```sh
http://127.0.0.1:8000/info_about_two_cities?city1=Новогребенщиково&city2=Новогеоргиевка
```
>Данные от сервера:
```
[
    {
        "geonameid": 1497093,
        "name": "Novogrebenshchikovo",
        "asciiname": "Novogrebenshchikovo",
        "alternatenames": "Novogrebenshchikovo,Novogrebenshhikovo,Novoye-Grebenshchikovo,Новогребенщиково",
        "latitude": 54.90167,
        "longitude": 78.5165,
        "feature class": "P",
        "feature code": "PPL",
        "country code": "RU",
        "cc2": "",
        "admin1 code": "53",
        "admin2 code": "",
        "admin3 code": "",
        "admin4 code": "",
        "population": 0,
        "elevation": "",
        "dem": "114",
        "timezone": "Asia/Novosibirsk",
        "modification date": "2012-01-17"
    },
    {
        "geonameid": 7687830,
        "name": "Novogeorgiyevka",
        "asciiname": "Novogeorgiyevka",
        "alternatenames": "Novo-Georgiyevsk,Novogeorgievka,Novogeorgiyevka,Новогеоргиевка",
        "latitude": 50.9407,
        "longitude": 38.4019,
        "feature class": "P",
        "feature code": "PPL",
        "country code": "RU",
        "cc2": "",
        "admin1 code": "09",
        "admin2 code": "",
        "admin3 code": "",
        "admin4 code": "",
        "population": 0,
        "elevation": "",
        "dem": "215",
        "timezone": "Europe/Moscow",
        "modification date": "2012-01-21"
    },
    {
        "same latitude": false,
        "on the north": "Novogrebenshchikovo"
    },
    {
        "same timezone": false,
        "difference": "-1 day, 20:00:00"
    }
]
```
#### Другие методы, реализованнные в программе:
 
 ```sh
def dict_maker(city):
```
   Данная функция получает на вход переменную city - список полей города, и преобразует ее в словарь для работы с объектами в дальнейшем. Возвращаемое значение - словарь.
   ```sh
def id_searcher(id_name):
```
Данная функция принимает id_name - geonameid искомого города. С помощью бинарного поиска оптимизирован алгоритм поиска города, так как в файле, с которым работает программа много данных. Функция возвращает индекс - позиция города в списке LIST_OF_CITIES, если город не найден, программа возвращает -1.
   ```sh
def name_searcher(ru_name):
```
Данная функция принимает ru_name - имя искомого города на русском языке. Функция проходит по списку городов и ищет элементы, у которых в графе alternatenamesприсутствует запрашиваемое имя, добавляя этот элемент в список result. Далее, если таких городов оказалось несколько, она сортирует их по популяции и выбирает город с большим населнием. Функция возвращает искомый город в виде словаряс помощью функции dict_maker, если города не нашлось, функция отправляет сообщение-исключение.
   ```sh
def page_maker(page_num, amount):
```
Данная функция принимает два параметра: page_num - номер искомой страницы, amount - количесво городов на странице. Если запрашиваемой страницы не существует, функция отправляет сообщение-исключение. Если страница неполная (например, последняя), то функция вернет список городов, приведенных к словарю с помошью функции dict_maker с меньшим или равным amount количеством объектов.
   ```sh
def compare_cities(city1, city2, param):
```
Данная функця принимает на вход city1, city2 - города-словари, которые требуют сравнения по параметру param. В данный момент осуществляется сравнение по параметрам: ширина, временная зона. Для param = 'latitude', функция сравнивает координатную широту городов и возвращает словарь: {'same latitude' = bool, 'on the north' = asciiname} 
Для param = 'timezone', функция сравнивает название временной зоны и с помощью библиотеки pytz и локализации времени находит разницу во времени между городами, если она сеть. Возвращает словарь: {'same timezone': bool, 'difference': str}
