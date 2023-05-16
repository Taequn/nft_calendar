from parsers.listings_parser.AbstractParser import AbstractParser
import pandas as pd
import json
import datetime
from urllib.request import Request, urlopen
import re
import logging

logging.basicConfig(level=logging.INFO)
class MintyScoreParser(AbstractParser):
    def get_name(self):
        return "mintyscore"
    
    def parse(self, filename=None, save=False):
        if filename is None:
            filename = "mintyscore_data"
        
        data = self.__mintyscore_parse()
        if save:
            data.to_csv(f"data/{filename}.csv", index=False)
        
        return data
    
    def __process_minty_entry(self, nft):
        try:
            date = nft['sale_date']
            date = datetime.datetime.strptime(
                date, '%Y-%m-%dT%H:%M:%S+00:00').strftime("%Y-%m-%d %H:%M:%S")
        except Exception as e:
            date = "TBA"

        name = nft['name']
        price = nft['price_info']
        if (price == '' or price == 'TBA'):
            price = 'TBA'
        else:
            try:
                price = re.findall(r'\d+\.\d+', price)
                price = ''.join(price)
            except Exception as e:
                price = 'TBA'

        discord = nft['discord_link']
        twitter = nft['twitter_link']
        link = nft['website_link']
        platform = nft['chain'].capitalize()

        image = nft['picture_link']

        try:
            supply = nft['supply_info']
            supply = re.findall(r'\d+', supply)
            supply = ''.join(supply)
        except Exception as e:
            logging.error('Error parsing supply')
            supply = ''
        
        return pd.DataFrame({"Date": date, "Link": link, "Collection": name,
                                "Discord": discord, "Twitter": twitter, "Supply": supply,
                                "Platform": platform, "Price": price, "Picture": image}, index=[0])
        
    def __mintyscore_parse(self):
        df = pd.DataFrame()
        logging.info('Checking mintyscore.com')

        url = 'https://api.mintyscore.com/api/v1/nfts/projects?desc=true&chain=all&status=upcoming&sort_by=like_count&include_hidden=false'
        request = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        response = urlopen(request).read()
        json_data = json.loads(response)
        nfts = json_data['result']

        for nft in nfts:
            df_entry = self.__process_minty_entry(nft)
            df = pd.concat([df, df_entry], ignore_index=True)
        df['Listing'] = 'MintyScore'
        logging.info('MintyScore check complete')
        return df

if __name__ == "__main__":
    parser = MintyScoreParser()
    parser.parse(save=True)