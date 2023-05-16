from parsers.listings_parser.AbstractParser import AbstractParser
import pandas as pd
import datetime
import logging

logging.basicConfig(level=logging.INFO)
class OxalusParser(AbstractParser):
    def get_name(self):
        return "oxalus"
    
    def parse(self, filename=None, save=False):
        if filename is None:
            filename = "oxalus_data"
        
        data = self.__oxalus()
        if save:
            data.to_csv(f"data/{filename}.csv", index=False)
        
        return data
         
    def __process_oxalus_entry(self, project):
        if project['date'] == 0:
            date = 'TBA'
        else:
            date = datetime.datetime.fromtimestamp(
                project['date']/1000).strftime("%Y-%m-%d %H:%M:%S")
        link = project['home_link']
        name = project['name']
        discord = ''
        twitter = ''
        supply = ''
        platform = project['chain_slug'].capitalize()
        price = str(project['price_value'])
        image = project['image_url']

        for channel in project['media_channels']:
            if channel['key'] == 'twitter':
                twitter = channel['link']
            if channel['key'] == 'discord':
                discord = channel['link'] 
        
        return pd.DataFrame({"Date": date, "Link": link, "Collection": name,
                                "Discord": discord, "Twitter": twitter, "Supply": supply,
                                "Platform": platform, "Price": price, "Picture": image}, index=[0])
    
    def __oxalus(self):
        df = pd.DataFrame()
        logging.info('Checking oxalus.io')

        today = int(datetime.datetime.today().timestamp() * 1000)
        url = 'https://analytics-api.oxalus.io/collection-events?from=' + \
            str(today) + '&limit=200&offset=0&name=&append_zero_from_date=true'
        
        json_data = self.get_json_data(url)
        projects = json_data['data']['records']

        for project in projects:
            df_entry = self.__process_oxalus_entry(project)
            df = pd.concat([df, df_entry], ignore_index=True)

        df['Listing'] = 'Oxalus.io'
        logging.info('Oxalus.io check complete')
        return df

if __name__ == "__main__":
    parser = OxalusParser()
    parser.parse(save=True)