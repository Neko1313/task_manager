from flask import Flask, request, jsonify
import aiohttp
import requests

app = Flask(__name__)

SERVICES = {
    'scrapy': 'http://scrapy:8002',
    'new_photo': 'http://new_photo:8001',
    "working_data" : "http://working_data:8003",
    "statistics" : "http://statistics:8004"
}

@app.after_request
async def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = 'http://localhost:3000'  # Разрешаем запросы с этого домена
    response.headers['Access-Control-Allow-Methods'] = 'POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response

async def async_get(url, params=None):
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as response:
            return await response.json(), response.status

async def async_post(url, json_data=None):
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=json_data) as response:
            return await response.json(), response.status

@app.route('/api/<service_name>/<path:path>', methods=['GET', 'POST'])
async def gateway(service_name, path):
    if service_name in SERVICES:
        service_url = SERVICES[service_name]
        url = f"{service_url}/{path}"

        if request.method == 'GET':
            response, status = await async_get(url, params=request.args)
        elif request.method == 'POST':
            response, status = await async_post(url, json_data=request.json)

        return jsonify(response), status

    else:
        return jsonify({'error': f'Service {service_name} not found'}), 404

@app.route('/parse', methods=['POST'])
async def parse():
    if request.method == 'POST':
        service_url = SERVICES["new_photo"]
        url = f"{service_url}/gen"
        response, status = await async_post(url, json_data=request.json)
        return jsonify(response), status
    else:
        return jsonify({'error': 'Invalid request method'}), 405

@app.route('/api/working_data/parse_xls', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    try:
        url = "http://working_data:8003/parse_xls"
        files = {'file': (file.filename, file)}
        response = requests.post(url, files=files)
        return jsonify(response.json()), response.status_code

    except Exception as e:
        print(f"Error while processing file: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/working_data/add_graph', methods=['POST'])
def working_data_add_graph():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    try:
        url = "http://working_data:8003/add_graph"
        files = {'file': (file.filename, file)}
        response = requests.post(url, files=files)
        return jsonify(response.json()), response.status_code

    except Exception as e:
        print(f"Error while processing file: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/scrapy/scrapy_new_spider/<path:path>', methods=['POST'])
def scrapy_new_spider(path):
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    try:
        url = f"http://scrapy:8002/scrapy_new_spider/{path}"
        files = {'file': (file.filename, file)}
        response = requests.post(url, files=files)
        return jsonify(response.json()), response.status_code

    except Exception as e:
        print(f"Error while processing file: {e}")
        return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
