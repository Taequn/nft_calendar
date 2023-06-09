from parsers.listings_parser.AlphaBotParser import AlphaBotParser
from parsers.listings_parser.CryptoParser import CryptoParser
from parsers.listings_parser.MintyScoreParser import MintyScoreParser
from parsers.listings_parser.OxalusParser import OxalusParser
from parsers.listings_parser.RarityToolsParser import RarityToolsParser
from parsers.listings_parser.SeaFloorParser import SeaFloorParser
from parsers.listings_parser.UpcomingNFTParser import UpcomingNFTParser
#Socials parsers
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
        elif name.lower() == "upcomingnft":
            return UpcomingNFTParser()
        elif name.lower() == "cryptocom":
            return CryptoParser()
        elif name.lower() == "raritytools":
            return RarityToolsParser()
        elif name.lower() == 'seafloor':
            return SeaFloorParser()
        else:
            raise ValueError(f"No listing parser found for {name}")
    
    def make_socials_parser(self, name):
        if name.lower() == "discord":
            return DiscordParser()
        elif name.lower() == "twitter":
            return TwitterParser()
        else:
            raise ValueError(f"No socials parser found for {name}")