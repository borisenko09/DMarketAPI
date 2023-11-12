# dmarket_py
dmarket_py
Описание
Библиотека для взаимодействия с сайтом dmarket.com которая использует api

Установка
Скачайте библиотеку с гитхаба, установите зависимости
Copy code
pip install pynacl
Быстрый старт
Пример быстрого начала работы с библиотекой. 

python
Copy code
# Пример кода
from dmarket_api import DMarketAPI

dmarket = DMarketAPI('your_public_key', 'your_secret_key')
response = dmarket.get_user_profile()
print(response)
Методы
Описание нескольких методов

get_user_profile()
Описание
Получение информации о профиле пользователя.

Пример использования
python
Copy code
user_profile = dmarket.get_user_profile()
print(user_profile)
get_user_balance()
Описание
Получение информации о балансе пользователя.

Пример использования
python
Copy code
user_balance = dmarket.get_user_balance()
print(user_balance)
Лицензия
MIT License
