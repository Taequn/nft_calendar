import pandas as pd
from urllib.request import Request, urlopen
import logging
from parsers.ParserProvider import ParserProvider


#logging.basicConfig(level=logging.INFO, filename='app.log', filemode='w')
logging.basicConfig(level=logging.INFO)

def run_listing_parser():
    parser = ParserProvider()
    try:
        df1 = parser.make_parser('alphabot').parse()
    except:
        df1 = pd.DataFrame()
        logging.error('Error checking alphabot.app')
    try:
        df2 = parser.make_parser('mintyscore').parse()
    except:
        df2 = pd.DataFrame()
        logging.error('Error checking mintyscore.com')
    try:
        df3 = parser.make_parser('oxalus').parse()
    except:
        df3 = pd.DataFrame()
        logging.error('Error checking oxalus.io')

    df = pd.concat([df1, df2, df3], ignore_index=True)
    df.to_csv('data/initial_parse.csv', index=False)
    #df.to_csv('parsers/go_code/file.csv')
    logging.info('Data saved to initial_parse.csv')


if __name__ == "__main__":
    run_listing_parser()
