from parsers.listings_parser.AbstractParser import AbstractParser
import pandas as pd
import datetime
import logging
import time

logging.basicConfig(level=logging.INFO)
class AlphaBotParser(AbstractParser):
    def get_name(self):
        return "alphabot"
    
    def parse(self, filename=None, save=False):
        if filename is None:
            filename = "alphabot_data"
        
        data = self.__alphabot()
        if save:
            data.to_csv(f"data/{filename}.csv", index=False)
        
        return data
        
    
    def __process_alpha_entry(self, entry):
        try:
            date = datetime.datetime.fromtimestamp(
                entry['mintDate']/1000).strftime("%Y-%m-%d %H:%M:%S")
        except:
            date = "TBA"

        collection = entry['name']
        link = ""

        try:
            discord = entry['discordUrl']
        except:
            discord = ""

        try:
            twitter = entry['twitterUrl']
        except:
            twitter = ""

        try:
            supply = entry['supply']
        except:
            supply = ""

        try:
            platform = entry['blockchain']
        except:
            platform = ""

        try:
            price = entry['pubPrice']
        except:
            price = ""

        try:
            picture = entry['twitterProfileImage']
        except:
            picture = ""

        return pd.DataFrame({"Date": date, "Link": link, "Collection": collection,
                            "Discord": discord, "Twitter": twitter, "Supply": supply,
                            "Platform": platform, "Price": price, "Picture": picture}, index=[0])
    
    def __alphabot(self):
        df = pd.DataFrame()
        logging.info('Checking alphabot.app')

        today = int(datetime.datetime.today().timestamp() * 1000)
        earliest_timestamp = today - (today % 86400000) + 86400000
        page_number = 0
        attempts = 0

        while True:
            if (page_number == 25):
                break
            logging.info("AlphaBot page " + str(page_number+1) + " checked")
            #print("AlphaBot page " + str(page_number) + " checked")

            url = 'https://www.alphabot.app/api/projectData/search?sort=mintDate&sortDir=1&pageNum=' + str(page_number) + '&search=&earliest=' + str(
                earliest_timestamp) + '&pageSize=24&blockchains=ETH&blockchains=SOL&blockchains=BTC&blockchains=VENOM&blockchains=MATIC&blockchains=SUI&blockchains=APT&blockchains=EGLD'

            json_data = self.get_json_data(url)

            # Error handling when failing to load data
            if (len(json_data) == 0):
                if (attempts < 5):
                    attempts += 1
                    logging.warning("AlphaBot page " + str(page_number) + " failed to load, retrying")
                    time.sleep(1)
                    continue
                logging.error("AlphaBot page " + str(page_number) + " failed to load, finishing check")
                break

            attempts = 0
            for entry in json_data:
                df_entry = self.__process_alpha_entry(entry)
                df = pd.concat([df, df_entry], ignore_index=True)

            page_number += 1

        df['Listing'] = 'Alphabot.app'
        logging.info('Alphabot.app check complete')
        return df

if __name__ == "__main__":
    parser = AlphaBotParser()
    parser.parse(save=True)