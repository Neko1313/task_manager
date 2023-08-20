import sqlite3

# Подключение к базе данных
db_connection = sqlite3.connect("./intermediate.db")
cursor = db_connection.cursor()

# Выполнение SQL-запроса для выборки всех данных из таблицы Books
cursor.execute("SELECT * FROM Books")
all_books = cursor.fetchall()

# Вывод результатов
for book in all_books:
    print(book)

# Закрытие соединения с базой данных
db_connection.close()
