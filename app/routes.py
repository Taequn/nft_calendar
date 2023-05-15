from flask import Flask, jsonify, request, abort
from functools import wraps
#import os
import pandas as pd
#from dotenv import load_dotenv

app = Flask(__name__)

#load_dotenv()
#API_KEY = os.getenv('API_KEY')

def require_api_key(view_function):
    @wraps(view_function)
    def decorated_function(*args, **kwargs):
        if request.args.get('key') and request.args.get('key') == API_KEY:
            return view_function(*args, **kwargs)
        else:
            abort(401)
    return decorated_function

#Запрос по формату: http://ADDRESS/api/v1/data?key=api_key
#Example: http://127.0.0.1:5000/api/v1/data?key=TAQ3pTivtFNVT1bxfcn2aCDVDY2wBvPgWwjXG80mJ7RUQoyQzKanH38z57VhqTTJ9Gv2jpC46
@app.route('/api/v1/data', methods=['GET'])
#@require_api_key
def get_data():
    #print(API_KEY)
    # Читаем данные, которые выгрузили из flask_parse.py
    data = pd.read_csv("data/enriched_data_results.csv").drop_duplicates(subset=['Collection']).to_dict(orient='records')
    # Возвращаем данные в формате JSON
    return jsonify(data)

if __name__ == '__main__':
    app.run(port=5000, debug=True)
