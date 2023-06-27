from parsers.listings_parser.AbstractParser import AbstractParser
import datetime
import pandas as pd
import logging
import json
from urllib.request import Request, urlopen

logging.basicConfig(level=logging.INFO)
class SeaFloorParser(AbstractParser):
    def get_name(self):
        return "seafloor"
    
    def parse(self, filename=None, save=False):
        if filename is None:
            filename = "seafloor_data"
        
        data = self.__seafloor_parse()
        if save:
            data.to_csv(f"data/{filename}.csv", index=False)
        
        return data
    
    def __process_seafloor_entry(self, nft):
        name = nft['name']
        try:
            date = nft['dateTime']
            date = datetime.datetime.strptime(date, '%B %d, %Y %I:%M %p GMT+8').strftime("%Y-%m-%d %H:%M:%S")
        except:
            date = "TBA"

        try: twitter = nft['twitter']
        except KeyError: twitter = ''

        try: discord = nft['discord']
        except KeyError: discord = ''

        try: link = nft['website']
        except KeyError: link = ''

        try: supply = nft['volume']
        except KeyError: supply = ''

        try:price = nft['mintPrice']
        except KeyError: price = ''

        try: platform = nft['platform']
        except KeyError: platform = ''
        
        try: image = nft['cover']
        except KeyError: image = ''

        return pd.DataFrame({"Date": date, "Link": link, "Collection": name,
                        "Discord": discord, "Twitter": twitter, "Supply": supply,
                        "Platform": platform, "Price": price.split(" ")[0], 
                        "Picture": image}, index=[0])
    
    def __seafloor_parse(self):
        df = pd.DataFrame()
        logging.info("Checking seafloor.io")

        url = 'https://seafloor.io/assets/js/collection_test.php'
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        webpage = urlopen(req).read()
        nfts = json.loads(webpage)
        for nft in nfts:
            df_entry = self.__process_seafloor_entry(nft)
            df = pd.concat([df, df_entry], ignore_index=True)
        
        df['Listing'] = "SeaFloor"
        return df
        