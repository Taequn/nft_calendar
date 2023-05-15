from flask import Flask
from app.api.run_parser_route import parser_api
from app.api.get_data_route import data_api

app = Flask(__name__)
app.register_blueprint(data_api, url_prefix='/api')
app.register_blueprint(parser_api, url_prefix='/api')

if __name__ == '__main__':
    app.run(port=5000, debug=True)