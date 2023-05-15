import sys
import os
import subprocess

# Add the root directory of your project to the Python module search path
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root_dir)

from nft_calendar.parsers.listing_parser import run_listing_parser
from nft_calendar.parsers.twitter_parser_go.go_execute import run_twitter_parser
from nft_calendar.parsers.discord_members_parser import enrich_collection_data

#run_listing_parser()
#run_twitter_parser()

enrich_collection_data()

