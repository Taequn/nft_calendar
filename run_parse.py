from app.utils.daily_parse import run_daily_parse
from parsers.listings_parser.listing_parser import run_listing_parser
from parsers.ParserProvider import ParserProvider
import sys

if __name__ == '__main__':
    action = sys.argv[1]
    parser = ParserProvider()
    
    if action == "listings":
        listing = sys.argv[2]
        if listing:
            parser.make_listing_parser(listing).parse()
        else:
            run_listing_parser()
    
    if action == "twitter":
        parser.make_socials_parser("twitter").parse()
    
    if action == "discord":
        parser.make_socials_parser("discord").parse()
    
    if action == "all":
        run_daily_parse()