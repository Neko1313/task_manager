from quart import Quart, jsonify, request
import subprocess

app = Quart(__name__)

@app.route('/gen', methods=['POST'])
async def gen():
    if request.method == 'POST':
        list_isbn = await request.json
        subprocess.Popen(["python", "./module/photo.py", f"{list_isbn}"], shell=False)
        return jsonify(list_isbn)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8001)
