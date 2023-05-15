from flask import Blueprint, jsonify, request, abort
from functools import wraps
import pandas as pd
import os
import concurrent.futures
from parsers.listing_parser import run_listing_parser
from parsers.twitter_parser_go.go_execute import run_twitter_parser
from parsers.discord_members_parser import enrich_collection_data
from daily_parse import run_daily_parse

api = Blueprint('api', __name__)

@api.route('/v1/data/<filename>', methods=['GET'])
def get_data(filename):
    data_dict = {
        "get_listings": "initial_parse",
        "get_twitter": "twitter_data",
        "get_discord": "parsed_discord_members",
        "get_everything": "enriched_data_results"
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


@api.route("v1/parser/<action>", methods=['GET'])
def run_parser(action):
    success_dict = {
        "action": action,
        "status": "success",
        "message": "Parser successfully started"
    }
    
    try:
        with concurrent.futures.ThreadPoolExecutor() as executor:
            if action == "listings":
                executor.submit(run_listing_parser)
            
            if action == "twitter":
                executor.submit(run_twitter_parser)
            
            if action == "discord":
                executor.submit(enrich_collection_data)
            
            if action == "all":
                executor.submit(run_daily_parse)
    except Exception as e:
            fail_dict = {
                "action": action,
                "status": "fail",
                "message": "Parser failed to start",
                "error": str(e)
            }
            return jsonify(fail_dict)
            
    return jsonify(success_dict)
