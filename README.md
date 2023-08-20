# Запуск 
В каждой папки кроме graph есть фаил requirements.txt переходим в каждую папку создаем вертуальное окружение 
## Бэк
1. Передите в модуль: ```cd api_gateway```
2. Создайте вертальное окружение: ```python -m venv venv```
3. Активируйте его: 
3.1 Linux и macOC: ```source venv/bin/activate```
3.2 Windows : ```venv\Scripts\activate```
4. Установите библиотеки : ```pip install -r requirements.txt```
5. Запуск : ```python app.py```

## Фронт
1. Передите в модуль: ```cd graph```
2. Установка зависимостей: ```npm install```
3. Запуск: ```npm start```

# Описание модулей
- api_gateway - Распределение запросов и очередь - :5000
- graph - Графический интерфейс - :3000
- new_photo - Создание и скачивание обложек - :8001
- scrapy - Пауки scrapy - :8002
- statistics - Создание графиков - :8004
- working_data - Сохранение промежуточных данных - :8003



