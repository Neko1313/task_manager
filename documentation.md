# API для системы пауков по модулям :bowtie:
## :one: new_photo
+ `POST` localhost:5000/api/new_photo/gen 
    - формат json который передается {"isbn" : "link_cover_with_other_site"}
    - скачивает фотографии и сохраняет их в нужны форматах
## :two: scrapy
+ `POST` localhost:5000/api/scrapy/photo 
    - формат json который передается ["isbn_1" , "isbn_2" , ...] 
    - Запускает пауков которые пробегут по этому листу isbn и соберут ссылки на изображения
+ `POST` localhost:5000/api/scrapy/des 
    - формат json который передается ["isbn_1" , "isbn_1" , ...] 
    - Запускает пауков которые пробегут по этому листу isbn и соберут описание
+ `POST` localhost:5000/api/scrapy/configuration_photo 
    - формат json который передается ["name_spider_1" , "name_spider_1" , ...] 
    - Переписывает очередь для пауков для фото
+ `GET` localhost:5000/api/scrapy/configuration_photo 
    - формат json который отдает ["name_spider_1" , "name_spider_1" , ...] 
    - Отдает очередь пауков для фото
+ `POST` localhost:5000/api/scrapy/configuration_des 
    - формат json который передается ["name_spider_1" , "name_spider_1" , ...] 
    - Переписывает очередь для пауков для описания
+ `GET` localhost:5000/api/scrapy/configuration_des 
    - формат json который отдает ["name_spider_1" , "name_spider_1" , ...] 
    - Отдает очередь пауков для описания 
+ `POST` localhost:5000/api/scrapy/scrapy_new_spider/photo 
    - принемает фаил 
    - Создает новый фаил паука для фото и добавляет его последным в очередь
+ `POST` localhost:5000/api/scrapy/scrapy_new_spider/des 
    - принемает фаил 
    - Создает новый фаил паука для описания и добавляет его последным в очередь
## :three: statistics
+ `GET` localhost:5000/api/statistics/static_all 
    - Отдает фаил графика 
    - Создает новые графики для вкладка статистика
## :four: working_data
+ `POST` localhost:5000/api/working_data/parse_xls 
    - Принемает фаил xls  
    - Сохраняет новые данные от "медленых книг" в промежуточную таблицу и отправляет запросы на поиск обложек и описаний 
+ `POST` localhost:5000/api/working_data/photo_found 
    - Принемает json {"isbn" : "the_path_to_the_cover_on_our_server"} 
    - Сохраняет в промежуточную таблицу обложки новых форматов
+ `POST` localhost:5000/api/working_data/photo_des 
    - Принемает json {"isbn" : "new_description"} 
    - Обновляет описание книг по их isbn
+ `GET` localhost:5000/api/working_data/get_all_data 
    - Оправлает json {"column_names" : ["column_name_1","column_name_1", ...], "data" : [["data_col_1","data_col_2", ...],["data_col_1","data_col_2", ...], ...]}
    - Получение всех данных которые есть сейчас в промежуточной таблицы
+ `POST` localhost:5000/api/working_data/add_graph 
    - Принемает фаил изображения графика
    - Приобразует в bytea и сохраняет в postgresql
+ `GET` localhost:5000/api/working_data/get_graph_data 
    - Отправяляет [{"id" : "graph_id", "image_data" : "img_graph", "access_date" : "date_of_creation_of_the_schedule"}, ...]
    - Отправляет графики для аналитики