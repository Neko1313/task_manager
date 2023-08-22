# API для системы пауков по модулям :shipit:
## new_photo
+ `POST` localhost:5000/api/new_photo/gen 
    - формат json который передается {"isbn" : "link_cover_with_other_site"}
    - скачивает фотографии и сохраняет их в нужны форматах
## scrapy
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