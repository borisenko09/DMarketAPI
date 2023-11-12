# dmarket_py
Библиотека для взаимодействия с сайтом dmarket.com которая использует api

Установка
Скачайте библиотеку с гитхаба, установите зависимости

pip install pynacl


# Пример кода
from dmarket_api import DMarketAPI

dmarket = DMarketAPI('your_public_key', 'your_secret_key')
response = dmarket.get_user_profile()
print(response)

# Несколько методов

- get_user_profile()

Получение информации о профиле пользователя.
  

user_profile = dmarket.get_user_profile()

print(user_profile)

- get_user_balance()

Получение информации о балансе пользователя.


user_balance = dmarket.get_user_balance() 

print(user_balance)

# Лицензия
GPL-3.0 license
