from flask import Flask, render_template
import pandas as pd
from app.api.run_parser_route import parser_api
from app.api.get_data_route import data_api

app = Flask(__name__)
app.register_blueprint(data_api, url_prefix='/api')
app.register_blueprint(parser_api, url_prefix='/api')

@app.route('/collections')
def collections():
    # Replace this with code to fetch data from your database
    data = pd.read_csv("data/enriched_data_results.csv").drop_duplicates(subset=['Collection']).to_dict(orient='records')
    return render_template('collections.html', data=data)