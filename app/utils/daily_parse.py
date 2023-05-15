import pandas as pd

from parsers.listing_parser import run_listing_parser
from parsers.twitter_parser_go.go_execute import run_twitter_parser
from parsers.discord_members_parser import enrich_collection_data

def run_daily_parse():
    run_listing_parser()
    run_twitter_parser()
    enrich_collection_data()

    df_final = pd.read_csv('data/initial_parse.csv').drop_duplicates(subset="Collection")

    df2 = pd.read_csv('data/parsed_discord_members.csv').drop_duplicates(subset="Collection")
    df_final = df_final.merge(df2[["Collection", "Discord Total Members", "Discord Online Members"]], on="Collection", how="left")

    df3 = pd.read_csv('data/twitter_data.csv').drop_duplicates(subset="Collection")
    df_final = df_final.merge(df3[["Collection", "Twitter Followers"]], on="Collection", how="left")

    df_final.to_csv('data/enriched_data_results.csv', index=False)
    


