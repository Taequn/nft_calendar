from parsers.listings_parser.AlphaBotParser import AlphaBotParser
from parsers.listings_parser.OxalusParser import OxalusParser
from parsers.listings_parser.MintyScoreParser import MintyScoreParser
from parsers.discord_parser.DiscordParser import DiscordParser
from parsers.twitter_parser_go.TwitterParser import TwitterParser

class ParserProvider:
    def make_listing_parser(self, name):
        if name.lower() == "mintyscore":
            return MintyScoreParser()
        elif name.lower() == "oxalus":
            return OxalusParser()
        elif name.lower() == "alphabot":
            return AlphaBotParser()
        else:
            raise ValueError(f"No listing parser found for {name}")
    
    def make_socials_parser(self, name):
        if name.lower() == "discord":
            return DiscordParser()
        elif name.lower() == "twitter":
            return TwitterParser()
        else:
            raise ValueError(f"No socials parser found for {name}")