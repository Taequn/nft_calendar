from flask import Blueprint, jsonify
from parsers.listings_parser.listing_parser import run_listing_parser
from parsers.twitter_parser_go import TwitterParser
from parsers.discord_parser import DiscordParser
from app.utils.daily_parse import run_daily_parse

parser_api = Blueprint('parser_api', __name__)

# The function run_parser is now associated with the Blueprint parser_api
@parser_api.route("v1/parser/<action>", methods=['GET'])
def run_parser(action):
    success_dict = {
        "action": action,
        "status": "success",
        "message": "Parser successfully started"
    }
    
    try:
        if action == "listings":
            run_listing_parser()
        
        if action == "twitter":
            twitter = TwitterParser()
            twitter.parse()
        
        if action == "discord":
            discord = DiscordParser()
            discord.parse()
        if action == "all":
            run_daily_parse()
    
    except Exception as e:
            fail_dict = {
                "action": action,
                "status": "fail",
                "message": "Parser failed to start",
                "error": str(e)
            }
            return jsonify(fail_dict)
            
    return jsonify(success_dict)
