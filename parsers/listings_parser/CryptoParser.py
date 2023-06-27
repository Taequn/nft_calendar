from parsers.listings_parser.AbstractParser import AbstractParser
import datetime
import pandas as pd
import logging
import json
from urllib.request import Request, urlopen

logging.basicConfig(level=logging.INFO)
class CryptoParser(AbstractParser):
    def get_name(self):
        return "cryptocom"
    
    def parse(self, filename=None, save=False):
        if filename is None:
            filename = "cryptocom_data"
        
        data = self.__crypto_parse()
        if save:
            data.to_csv(f"data/{filename}.csv", index=False)
        
        return data
    
    def __process_crypto_entry(self, nft):
        name = nft['collection']
        try:
            date = nft['release_date']
            date = datetime.datetime.fromtimestamp(date).strftime("%Y-%m-%d %H:%M:%S")
        except:
            date = nft['release_date']

        twitter = nft['twitter_url']
        discord = nft['discord_url']
        platform = nft['blockchain']
        supply = nft['assets']
        price = nft['mint_price']
        link = nft['website_url']
        image = nft['image_address'][0]

        return pd.DataFrame({"Date": date, "Link": link, "Collection": name,
                        "Discord": discord, "Twitter": twitter, "Supply": supply,
                        "Platform": platform, "Price": price, "Picture": image}, index=[0])
    
    def __crypto_parse(self):
        df = pd.DataFrame()
        logging.info("Checking Crypto.com")

        iteration = True
        page_number = 1
        while iteration:
            url = 'https://price-api.crypto.com/nft/v1/calendar/upcoming?page={}&type=1&limit=20'.format(page_number)
            request = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            response = urlopen(request).read()
            json_data = json.loads(response)
            nfts = json_data['data']['data']
            if(len(nfts) <= 20):
                iteration = False
            else:
                page_number += 1
        
            for nft in nfts:
                df_entry = self.__process_crypto_entry(nft)
                df = pd.concat([df, df_entry], ignore_index=True)
        
        df['Listing'] = 'Crypto.com'
        return df