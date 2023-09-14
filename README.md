# Задание
Нужно разработать микросервис для BookCourt по автоматизации сбора дополнительной информации о книгах партнеров 

# Запуск 
Всё уже настроено нужно только запустить docker-compose для этого поочередно вводем команды
```
docker-compose build
```
И 
```
docker-compose up
```

# Описание модулей
- api_gateway - Распределение запросов и очередь - :5000
- graph - Графический интерфейс - :3000
- new_photo - Создание и скачивание обложек - :8001
- scrapy - Пауки scrapy - :8002
- statistics - Создание графиков - :8004
- working_data - Сохранение промежуточных данных - :8003

# Доп. информация
Графики сейчас хранять в bytea в postgresql 
В таблицы :
```
CREATE TABLE AccessDates (
    id SERIAL PRIMARY KEY,
    chart BYTEA NOT NULL,
    access_date TIMESTAMP NOT NULL
);
```

[Ссылка на документацию по api](./documentation.md)
