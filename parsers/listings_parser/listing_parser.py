import pandas as pd
from urllib.request import Request, urlopen
import logging
from parsers.ParserProvider import ParserProvider


#logging.basicConfig(level=logging.INFO, filename='app.log', filemode='w')
logging.basicConfig(level=logging.INFO)

def run_listing_parser():
    parser_names = ['mintyscore', 'oxalus', 'alphabot', 
                    'upcomingnft', 'cryptocom',
                    'raritytools', 'seafloor']
    df_array = []
    parser = ParserProvider()
    
    for name in parser_names:
        try:
            df = parser.make_listing_parser(name).parse()
            df_array.append(df)
        except:
            logging.error(f'Error parsing {name}')
    
    
    df = pd.concat(df_array, ignore_index=True)
    df.to_csv('data/initial_parse.csv', index=False)
    df.to_csv('parsers/twitter_parser_go/file.csv')
    logging.info('Data saved to initial_parse.csv')


if __name__ == "__main__":
    run_listing_parser()
