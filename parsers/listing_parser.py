import requests
import json
import datetime
import pandas as pd
from urllib.request import Request, urlopen
import re
import logging

#logging.basicConfig(level=logging.INFO, filename='app.log', filemode='w')
logging.basicConfig(level=logging.INFO)

def get_json_data(url):
    response = requests.get(url)
    return json.loads(response.content)

#######################
### DATA PROCESSING ###
#######################
def process_alpha_entry(entry):
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

def process_minty_entry(nft):
    try:
        date = nft['sale_date']
        date = datetime.datetime.strptime(
            date, '%Y-%m-%dT%H:%M:%S+00:00').strftime("%Y-%m-%d %H:%M:%S")
    except:
        return

    name = nft['name']
    price = nft['price_info']
    if (price == '' or price == 'TBA'):
        price = 'TBA'
    else:
        price = re.findall(r'\d+\.\d+', price)
        price = ''.join(price)

    discord = nft['discord_link']
    twitter = nft['twitter_link']
    link = nft['website_link']
    platform = nft['chain'].capitalize()

    image = nft['picture_link']

    try:
        supply = nft['supply_info']
        supply = re.findall(r'\d+', supply)
        supply = ''.join(supply)
    except:
        supply = ''
    
    return pd.DataFrame({"Date": date, "Link": link, "Collection": name,
                            "Discord": discord, "Twitter": twitter, "Supply": supply,
                            "Platform": platform, "Price": price, "Picture": image}, index=[0])

def process_oxalus_entry(project):
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

#######################
### DATA COLLECTION ###
#######################
def alphabot():
    df = pd.DataFrame()
    logging.info('Checking alphabot.app')

    today = int(datetime.datetime.today().timestamp() * 1000)
    earliest_timestamp = today - (today % 86400000) + 86400000
    page_number = 0
    attempts = 0

    while True:
        if (page_number == 25):
            break
        logging.info("AlphaBot page " + str(page_number) + " checked")
        #print("AlphaBot page " + str(page_number) + " checked")

        url = 'https://www.alphabot.app/api/projectData/search?sort=mintDate&sortDir=1&pageNum=' + str(page_number) + '&search=&earliest=' + str(
            earliest_timestamp) + '&pageSize=24&blockchains=ETH&blockchains=SOL&blockchains=BTC&blockchains=VENOM&blockchains=MATIC&blockchains=SUI&blockchains=APT&blockchains=EGLD'

        json_data = get_json_data(url)

        # Error handling when failing to load data
        if (len(json_data) == 0):
            if (attempts < 5):
                attempts += 1
                logging.warning("AlphaBot page " + str(page_number) + " failed to load, retrying")
                continue
            logging.error("AlphaBot page " + str(page_number) + " failed to load, finishing check")
            break

        attempts = 0
        for entry in json_data:
            df_entry = process_alpha_entry(entry)
            df = pd.concat([df, df_entry], ignore_index=True)

        page_number += 1

    df['Listing'] = 'Alphabot.app'
    logging.info('Alphabot.app check complete')
    return df


def mintyscore():
    df = pd.DataFrame()
    logging.info('Checking mintyscore.com')

    url = 'https://api.mintyscore.com/api/v1/nfts/projects?desc=true&chain=all&status=upcoming&sort_by=like_count&include_hidden=false'
    request = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    response = urlopen(request).read()
    json_data = json.loads(response)
    nfts = json_data['result']

    for nft in nfts:
        df_entry = process_minty_entry(nft)
        df = pd.concat([df, df_entry], ignore_index=True)
    df['Listing'] = 'MintyScore'
    logging.info('MintyScore check complete')
    return df


def oxalus():
    df = pd.DataFrame()
    logging.info('Checking oxalus.io')

    today = int(datetime.datetime.today().timestamp() * 1000)
    url = 'https://analytics-api.oxalus.io/collection-events?from=' + \
        str(today) + '&limit=200&offset=0&name=&append_zero_from_date=true'
    
    json_data = get_json_data(url)
    projects = json_data['data']['records']

    for project in projects:
        df_entry = process_oxalus_entry(project)
        df = pd.concat([df, df_entry], ignore_index=True)

    df['Listing'] = 'Oxalus.io'
    logging.info('Oxalus.io check complete')
    return df


def run_listing_parser():
    try:
        df1 = alphabot()
    except:
        df1 = pd.DataFrame()
        logging.error('Error checking alphabot.app')
    try:
        df2 = mintyscore()
    except:
        df2 = pd.DataFrame()
        logging.error('Error checking mintyscore.com')
    try:
        df3 = oxalus()
    except:
        df3 = pd.DataFrame()
        logging.error('Error checking oxalus.io')

    df = pd.concat([df1, df2, df3], ignore_index=True)
    df.to_csv('data/initial_parse.csv', index=False)
    dt.to_csv('parsers/go_code/file.csv')
    logging.info('Data saved to initial_parse.csv')


if __name__ == "__main__":
    run_listing_parser()
