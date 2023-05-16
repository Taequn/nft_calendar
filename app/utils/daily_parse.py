import pandas as pd
import logging
from parsers.ParserProvider import ParserProvider

logging.basicConfig(level=logging.INFO)
def run_daily_parse():
    parser = ParserProvider()
    try:
        df1 = parser.make_listing_parser('alphabot').parse()
    except:
        df1 = pd.DataFrame()
        logging.error('Error checking alphabot.app')
    try:
        df2 = parser.make_listing_parser('mintyscore').parse()
    except:
        df2 = pd.DataFrame()
        logging.error('Error checking mintyscore.com')
    try:
        df3 = parser.make_listing_parser('oxalus').parse()
    except:
        df3 = pd.DataFrame()
        logging.error('Error checking oxalus.io')

    df = pd.concat([df1, df2, df3], ignore_index=True)
    df.to_csv('data/initial_parse.csv', index=False)
    df.to_csv('parsers/twitter_parser_go/file.csv')
    logging.info('Data saved to initial_parse.csv')
    
    parser.make_socials_parser("twitter").parse()
    parser.make_socials_parser("discord").parse()

    df_final = pd.read_csv('data/initial_parse.csv').drop_duplicates(subset="Collection")

    df2 = pd.read_csv('data/parsed_discord_members.csv').drop_duplicates(subset="Collection")
    df_final = df_final.merge(df2[["Collection", "Discord Total Members", "Discord Online Members"]], on="Collection", how="left")

    df3 = pd.read_csv('data/twitter_data.csv').drop_duplicates(subset="Collection")
    df_final = df_final.merge(df3[["Collection", "Twitter Followers"]], on="Collection", how="left")

    df_final.to_csv('data/enriched_data_results.csv', index=False)
    


