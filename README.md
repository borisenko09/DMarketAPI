## Обзор
`dmarket_py` - это библиотека для взаимодействия с сайтом [dmarket.com](https://dmarket.com), реализованная на основе их [API](https://docs.dmarket.com/v1/swagger.html). Эта библиотека позволяет упростить процесс выполнения различных операций на платформе DMarket.

## Установка
1. Клонируйте репозиторий с GitHub:
   ```git clone https://github.com/borisenko09/dmarket_py```
3. Установите необходимые зависимости: ```pip install pynacl```
## Начало работы
Для использования библиотеки импортируйте `DMarketAPI` и создайте экземпляр с вашими ключами доступа:
```python
from dmarket_api import DMarketAPI

dmarket = DMarketAPI('your_public_key', 'your_secret_key')
```
## Примеры использования
Получение информации о профиле пользователя
```python
user_profile = dmarket.get_user_profile()
print(user_profile)
```

Получение информации о балансе пользователя.
```python
user_balance = dmarket.get_user_balance() 
print(user_balance)
```
Реализованы все методы API которые доступны на офицально сайте, что бы узнать о них подробнее откройте [API](https://docs.dmarket.com/v1/swagger.html)

# Лицензия
GPL-3.0 license

# Поддержка
Если у вас возникли вопросы или предложения, пожалуйста, создайте новый issue в репозитории на GitHub.
