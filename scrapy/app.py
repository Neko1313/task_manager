from quart import Quart, jsonify, request
import asyncio
import aiosqlite
import subprocess
import json

app = Quart(__name__)

async def insert_to_db(queue, list_isbn):
    async with aiosqlite.connect('./task/task_isbn_photo.db') as conn:
        async with conn.cursor() as cursor:
            insert_query = '''
                INSERT INTO task (isbn)
                VALUES (?)
            '''
            await cursor.executemany(insert_query, [(isbn,) for isbn in list_isbn])
        await conn.commit()
    await queue.put(None)

async def insert_to_db_des(queue, list_isbn):
    async with aiosqlite.connect('./task/task_isbn_des.db') as conn:
        async with conn.cursor() as cursor:
            insert_query = '''
                INSERT INTO task (isbn)
                VALUES (?)
            '''
            await cursor.executemany(insert_query, [(isbn,) for isbn in list_isbn])
        await conn.commit()
    await queue.put(None)

async def start_spider():
    with open("./photo/queue.json", "r") as file:
        queue = json.load(file)
    
    subprocess.Popen(["python", f"./photo/{queue[0]}.py", "0"], shell=False)
    
async def start_spider_des():
    with open("./des/queue.json", "r") as file:
        queue = json.load(file)
    
    subprocess.Popen(["python", f"./des/{queue[0]}.py", "0"], shell=False)

@app.route('/photo', methods=['POST'])
async def photo():
    if request.method == 'POST':
        list_isbn = await request.json
        task_queue = asyncio.Queue()
        asyncio.create_task(insert_to_db(task_queue, list_isbn))
        asyncio.create_task(start_spider())
        return jsonify(list_isbn)
    
@app.route('/des', methods=['POST'])
async def des():
    if request.method == 'POST':
        list_isbn = await request.json
        task_queue = asyncio.Queue()
        asyncio.create_task(insert_to_db_des(task_queue, list_isbn))
        asyncio.create_task(start_spider_des())
        return jsonify(list_isbn)

@app.route('/configuration_photo', methods=['POST','GET'])
async def configuration_photo():
    if request.method == 'POST':
        spider_queue = await request.json
        with open("./photo/queue.json", 'w') as json_file:
            json.dump(spider_queue, json_file, indent=4)
        return jsonify(spider_queue)
    elif request.method == 'GET':
        with open("./photo/queue.json", 'r') as json_file:
            data = json.load(json_file)
        
        return jsonify(data)
    
@app.route('/configuration_des', methods=['POST','GET'])
async def configuration_des():
    if request.method == 'POST':
        spider_queue = await request.json
        with open("./des/queue.json", 'w') as json_file:
            json.dump(spider_queue, json_file, indent=4)
        return jsonify(spider_queue)
    elif request.method == 'GET':
        with open("./des/queue.json", 'r') as json_file:
            data = json.load(json_file)
        
        return jsonify(data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8002)
