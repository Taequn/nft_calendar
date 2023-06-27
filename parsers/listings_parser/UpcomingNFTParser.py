from parsers.listings_parser.AbstractParser import AbstractParser
from urllib.request import Request, urlopen
import datetime
import pandas as pd
import json
import logging

logging.basicConfig(level=logging.INFO)
class UpcomingNFTParser(AbstractParser):
    def get_name(self):
        return "upcomingnft"
    
    def parse(self, filename=None, save=False):
        if filename is None:
            filename = "upcomingnft_data"
        
        data = self.__upcomingNFT_parse()
        if save:
            data.to_csv(f"data/{filename}.csv", index=False)
    
    def __upcomingNFT_parse(self):
        df = pd.DataFrame()
        logging.info("Checking UpcomingNFT.net")

        url = 'https://upcomingnft.net/wp-json/wp/v2/event/calender'
        r = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        response = urlopen(r).read()
        json_data = json.loads(response)
        for data in json_data:
            df_entry = self.__process_UNFT_entry(data)
            df = pd.concat([df, df_entry], ignore_index=True)
        df['Listing'] = 'UpcomingNFT.net'
        return df
    
    
    def __process_UNFT_entry(self, data):
        try:
            data["public_date"] = datetime.datetime.strptime(data["public_date"], '%d %b %Y-%I:%M %p (UTC)').strftime('%Y-%m-%d %H:%M:%S')
        except ValueError:
            data['public_date'] = "TBA"

        return pd.DataFrame({"Date": data["public_date"], "Link": data["thundergamestudio_url"], "Collection": data["title"],
                             "Discord": data["discord_url"], "Twitter": data["twitter_url"], "Supply": data["wpcf-event-supply"],
                             "Platform": "Ethereum", "Price": data["wpcf-price"], "Picture": data['image']}, index=[0])
    
    