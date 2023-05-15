from flask import Blueprint, jsonify, abort
import pandas as pd
import os

data_api = Blueprint('data_api', __name__)

# The function get_data is now associated with the Blueprint data_api
@data_api.route('/v1/data/<filename>', methods=['GET'])
def get_data(filename):
    data_dict = {
        "listings": "initial_parse",
        "twitter": "twitter_data",
        "discord": "parsed_discord_members",
        "all": "enriched_data_results"
    }
    
    # Checks
    if filename not in data_dict:
        print(f"Invalid filename: {filename}")
        abort(404)
    if not os.path.isfile(f"data/{data_dict[filename]}.csv"):
        print(f"File not found: {filename}")
        abort(404)
    
    # Load CSV file
    data = pd.read_csv(f"data/{data_dict[filename]}.csv").drop_duplicates(subset=['Collection']).to_dict(orient='records')
    return jsonify(data)