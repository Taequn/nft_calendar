from parsers.listings_parser.AlphaBotParser import AlphaBotParser
from parsers.listings_parser.CoinMarketCapParser import CoinMarketCapParser
from parsers.listings_parser.CryptoParser import CryptoParser
from parsers.listings_parser.IcyToolsParser import IcyToolsParser
from parsers.listings_parser.MintyScoreParser import MintyScoreParser
from parsers.listings_parser.OxalusParser import OxalusParser
from parsers.listings_parser.RarityToolsParser import RarityToolsParser
from parsers.listings_parser.SeaFloorParser import SeaFloorParser
from parsers.listings_parser.UpcomingNFTParser import UpcomingNFTParser
from parsers.listings_parser.DiscordParser import DiscordParser


class ParserProvider:
    def make_listing_parser(self, name):
        if name.lower() == "mintyscore":
            return MintyScoreParser()
        elif name.lower() == "oxalus":
            return OxalusParser()
        elif name.lower() == "alphabot":
            return AlphaBotParser()
        elif name.lower() == "coinmarketcap":
            return CoinMarketCapParser()
        elif name.lower() == "upcomingnft":
            return UpcomingNFTParser()
        elif name.lower() == "cryptocom":
            return CryptoParser()
        elif name.lower() == "icytools":
            return IcyToolsParser()
        elif name.lower() == "raritytools":
            return RarityToolsParser()
        elif name.lower() == 'seafloor':
            return SeaFloorParser()
        elif name.lower() == "discord":
            return DiscordParser()
        
        
        else:
            raise ValueError(f"No listing parser found for {name}")