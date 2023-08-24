from quart import Quart, request, jsonify
import pandas as pd
import io
import sqlite3
import requests as req
from datetime import datetime
import psycopg2
import base64

app = Quart(__name__)

def check(char):
    valid_chars = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ',']
    return char in valid_chars

def keep_only_digits(value):
    if isinstance(value, str):
        return ''.join(filter(check, value))
    return ''

@app.route('/parse_xls', methods=['POST'])
async def parse_xls():
    if request.method == 'POST':
        if 'file' not in (await request.files):
            return jsonify({'error': 'No file part'}), 400

        file = (await request.files)['file']
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400
        
        file_contents = file.read()
        virtual_file = io.BytesIO(file_contents)
        df = pd.read_excel(virtual_file)
        df = df.drop(0).reset_index(drop=True)
        df = df.set_axis(df.iloc[0], axis=1)
        df = df.drop(0).reset_index(drop=True)
        df = df.drop_duplicates().reset_index(drop=True)
        df = df[["ISBN", "Автор", "Название", "Издательство", "Аннотация", "Год", "Цена", "Тип обл.", "Вес"]]
        df.rename(columns={
            "ISBN" : "isbn", 
            "Автор": "author", 
            "Название" : "title", 
            "Издательство" : "publisher", 
            "Аннотация" : "description", 
            "Год" : "publication_year", 
            "Цена" : "price", 
            "Тип обл." : "format", 
            "Вес" : "weight"
            }, inplace=True)
        df["photo"] = 0
        df["isbn"] = df["isbn"].apply(keep_only_digits)
        conn = sqlite3.connect('intermediate.db')
        df.to_sql('Books', conn, if_exists='append', index=False)
        conn.close()
        req.post("http://api_gateway:5000/api/scrapy/photo", json=df['isbn'].tolist())
        req.post("http://api_gateway:5000/api/scrapy/des", json=df.loc[df['description'].isnull(), 'isbn'].tolist())
        
        return jsonify({"ok": "200"}), 200

@app.route('/photo_found', methods=['POST'])
async def photo_found():
    if request.method == 'POST':
        db_connection = sqlite3.connect("intermediate.db")
        cursor = db_connection.cursor()
        data = await request.json
        cursor.execute("INSERT INTO BookImages (isbn, image_url) VALUES (?, ?)", (list(data.keys())[0], list(data.values())[0]))
        
        cursor.execute("UPDATE Books SET photo = ? WHERE isbn = ?",(1, list(data.keys())[0]))
        
        db_connection.commit()
        db_connection.close()
        
        return jsonify({"ok": "200"}), 200
    
@app.route('/photo_des', methods=['POST'])
async def photo_des():
    if request.method == 'POST':
        db_connection = sqlite3.connect("intermediate.db")
        cursor = db_connection.cursor()
        data = await request.json
        
        cursor.execute("UPDATE Books SET description = ? WHERE isbn = ?",(list(data.values())[0], list(data.keys())[0]))
        
        db_connection.commit()
        db_connection.close()
        
        return jsonify({"ok": "200"}), 200

@app.route('/get_all_data', methods=['GET'])
async def get_all_data():
    if request.method == 'GET':
        db_connection = sqlite3.connect("intermediate.db")
        cursor = db_connection.cursor()
        cursor.execute("SELECT * FROM Books")
        all_books = cursor.fetchall()
        column_names = [description[0] for description in cursor.description]
        
        db_connection.close()
        
        return jsonify({"column_names" : column_names, "data" : all_books}), 200

@app.route('/add_graph', methods=['POST'])
async def add_graph():
    if request.method == 'POST':
        if 'file' not in (await request.files):
            return jsonify({'error': 'No file part'}), 400

        file = (await request.files)['file']
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400
        
        image_data = file.read()
        conn = psycopg2.connect(database="mydb", user="neko", password="1313", host="postgres", port="5432")
        cur = conn.cursor()
        
        current_time = datetime.now()
        cur.execute("INSERT INTO AccessDates (chart, access_date) VALUES (%s, %s)", (psycopg2.Binary(image_data), current_time))
        
        conn.commit()
        conn.close()
        
        return jsonify({"column_names": "200"}), 200

@app.route('/get_graph_data', methods=['GET'])
def get_graph_data():
    try:
        conn = psycopg2.connect(database="mydb", user="neko", password="1313", host="postgres", port="5432")
        cur = conn.cursor()

        start_date = request.args.get('start')
        end_date = request.args.get('end')

        query = "SELECT id, chart, access_date FROM AccessDates"
        params = []
        if start_date and end_date:
            query += " WHERE access_date BETWEEN %s AND %s"
            params = [start_date, end_date]
        
        cur.execute(query, params)

        graph_data = []
        for row in cur.fetchall():
            graph_id, image_data, access_date = row
            graph_data.append({
                'id': graph_id,
                'image_data': base64.b64encode(image_data).decode('utf-8'),
                'access_date': access_date.strftime('%Y-%m-%d %H:%M:%S')
            })

        conn.close()

        return jsonify(graph_data)

    except Exception as e:
        return jsonify({'error': str(e)}), 500



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8003)
