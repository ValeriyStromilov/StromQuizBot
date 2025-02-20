import json
DICT_DATA = "data/quiz_data.json"
quiz_data = [
    {
        'question': 'Что такое Python?',
        'options': ['Язык программирования', 'Тип данных', 'Музыкальный инструмент', 'Змея на английском'],
        'correct_option': 0
    },
    {
        'question': 'Какой тип данных используется для хранения целых чисел?',
        'options': ['int', 'float', 'str', 'natural'],
        'correct_option': 0
    },
    {
        'question': 'Какой из перечисленных редакторов трёхмерной графики является бесплатным?',
        'options': ['Autodesk 3ds Max', 'Blender', 'Maya', 'Cinema 4D'],
        'correct_option': 1
    },
    {
        'question': 'Какая из перечисленных разработчиков игр, также занимается разработкой бухгалтерских программ?',
        'options': ['Cyberia Nova', 'EA Games', 'Nintendo', '1С'],
        'correct_option': 3
    },
    {
        'question': 'Как называется краткое изложение сути Python, встроенное в него самого?',
        'options': ['Писание', 'Ликбез', 'Дзен', 'Кодекс'],
        'correct_option': 2
    },
    {
        'question': 'Какая библиотека Python отвечает за асинхронное программирование?',
        'options': ['matplotlib', 'asyncio', 'TensorFlow', 'pillow'],
        'correct_option': 1
    },
    {
        'question': 'Какой тип наборов данных в Python обозначается квадратными скобками ([])?',
        'options': ['Список', 'Словарь', 'Кортеж', 'Множество'],
        'correct_option': 0
    },
    {
        'question': 'Каким образом в Python обозначается равенство?',
        'options': ['=', 'is', '==', '!='],
        'correct_option': 2
    },
    {
        'question': 'Что делает функция "range"?',
        'options': ["Объединеняет списки",
            "Генерирует список в опр. диапазоне",
            "Фильтрует элементы объекта",
            "Возвращает число эл-тов в указанном объекте-контейнере"],
        'correct_option': 1
    },
    {
        'question': 'Какая функция проверяет, состоит ли строка только из букв и чисел?',
        'options': ['lstrip', 'isalnum', 'isnumeric', 'format'],
        'correct_option': 1
    },
    {
        'question': 'Как называется функция, которая может быть определена в одной строке и без ключевого слова "def"?',
        'options': ['Альфа-функция', 'Бета-функция', 'Ипсилон-функция', 'Лямбда-функция'],
        'correct_option': 3
    },
    {
        'question': 'Что делает функция "len"?',
        'options': ['Преобразует число в двоичную строку', 'Возвращает кол-во эл-тов в объекте', 'Преобразует число в 16-ичную строку', 'Создаёт атрибут объекта'],
        'correct_option': 1
    }
]

with open(DICT_DATA, 'w') as file:
    json.dump(quiz_data, file)