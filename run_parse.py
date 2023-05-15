from app.utils.daily_parse import run_daily_parse
from parsers.listing_parser import run_listing_parser
from parsers.twitter_parser_go.go_execute import run_twitter_parser
from parsers.discord_members_parser import enrich_collection_data
import sys

if __name__ == '__main__':
    action = sys.argv[1]
    
    if action == "listings":
        run_listing_parser()
    
    if action == "twitter":
        run_twitter_parser()
    
    if action == "discord":
        enrich_collection_data()
    
    if action == "all":
        run_daily_parse()