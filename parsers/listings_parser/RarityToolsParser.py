from parsers.listings_parser.AbstractParser import AbstractParser
import datetime
import pandas as pd
import logging
import json
from urllib.request import Request, urlopen

logging.basicConfig(level=logging.INFO)
class RarityToolsParser(AbstractParser):
    def get_name(self):
        return "rarity_tools"
    
    def parse(self, filename=None, save=False):
        if filename is None:
            filename = "raritytools_data"
        
        data = self.__raritytools_parse()
        if save:
            data.to_csv(f"data/{filename}.csv", index=False)
        
        return data
    
    def __process_raritytools_entry(self, nft):
        name = nft['Project']
        try:
            date = nft['Sale Date']
            date = datetime.datetime.strptime(date, '%Y-%m-%dT%H:%M:%S.%fZ').strftime("%Y-%m-%d %H:%M:%S")
        except:
            date = 'TBA'

        try: twitter = nft['TwitterId']
        except KeyError: twitter = ''

        try: discord = nft['Discord']
        except KeyError: discord = ''

        try: link = nft['Website']
        except KeyError: link = ''

        try: supply = nft['Max Items']
        except KeyError: supply = ''

        try:price = nft['Price']
        except KeyError: price = ''
        
        try:
            platform = nft['Price Text']

            if 'SOL' in platform:
                platform = 'Solana'
            elif 'ETH' in platform:
                platform = 'Ethereum'
            elif 'ADA' in platform:
                platform = 'Cardano'
            elif 'TBA' in platform:
                price = 'TBA'
                platform = ''
            else:
                platform = ''
        except: platform = 'Ethereum'
        

        return pd.DataFrame({"Date": date, "Link": link, "Collection": name,
                        "Discord": discord, "Twitter": twitter, "Supply": supply,
                        "Platform": platform, "Price": price}, index=[0])
    
    def __raritytools_parse(self):
        df = pd.DataFrame()
        logging.info("Checking rarity.tools")
        url = 'https://collections.rarity.tools/upcoming2'
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        webpage = urlopen(req).read()
        data = json.loads(webpage)
        nfts = data[2:]
        for nft in nfts:
            df_entry = self.__process_raritytools_entry(nft)
            df = pd.concat([df, df_entry], ignore_index=True)
        
        df['Listing'] = "RarityTools"
        return df
        