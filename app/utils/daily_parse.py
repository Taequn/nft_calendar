import pandas as pd
import logging
from parsers.ParserProvider import ParserProvider
from parsers.listings_parser.listing_parser import run_listing_parser

logging.basicConfig(level=logging.INFO)
def run_daily_parse():
    run_listing_parser()
    
    parser = ParserProvider()
    
    parser.make_socials_parser("twitter").parse()
    parser.make_socials_parser("discord").parse()

    df_final = pd.read_csv('data/initial_parse.csv').drop_duplicates(subset="Collection")

    df2 = pd.read_csv('data/parsed_discord_members.csv').drop_duplicates(subset="Collection")
    df_final = df_final.merge(df2[["Collection", "Discord Total Members", "Discord Online Members"]], on="Collection", how="left")

    df3 = pd.read_csv('data/twitter_data.csv').drop_duplicates(subset="Collection")
    df_final = df_final.merge(df3[["Collection", "Twitter Followers"]], on="Collection", how="left")

    df_final.to_csv('data/enriched_data_results.csv', index=False)
    


