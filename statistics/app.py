from quart import Quart, request, jsonify
import pandas as pd
import requests as req
import matplotlib.pyplot as plt
import io

app = Quart(__name__)

@app.route('/static_all', methods=['GET'])
async def static_all():
    if request.method == 'GET':
        data = req.get("http://127.0.0.1:5000/api/working_data/get_all_data").json()
        df = pd.DataFrame(data['data'], columns=data['column_names'])
        df = df.replace(0, None)
        
        fill_percent = (df.count() / len(df)) * 100
        plt.figure(figsize=(10, 6))
        bars = plt.bar(fill_percent.index, fill_percent.values, color='c')
        plt.ylabel('Процент заполняемости')
        plt.ylim(0, 100)
        for bar in bars:
            yval = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2, yval + 2, round(yval, 2), ha='center', va='bottom', fontsize=10)
        
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        image_buffer = io.BytesIO()
        plt.savefig(image_buffer, format='png')
        
        # Создайте объект мультипартового запроса и добавьте файл
        files = {'file': ('graph.png', image_buffer.getvalue(), 'image/png')}
        req.post("http://127.0.0.1:5000/api/working_data/add_graph", files=files)
        
        return jsonify({"ok": "200"}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8004)
