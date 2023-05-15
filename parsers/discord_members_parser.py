import requests
import json
import time
import pandas as pd

def get_guild_members(inite_link):
    members = {
        "approximate_member_count": "N/A",
        "approximate_presence_count": "N/A"
    }
    
    if "discord" not in inite_link:
        return members
    
    
    guild_name = inite_link.split("/")[-1]
    
    discord_api_url = "https://discord.com/api/v9/invites/" + guild_name + "?with_counts=true&with_expiration=true"
    request = requests.get(discord_api_url)
    
    try:
        members = {
            "approximate_member_count": request.json()["approximate_member_count"],
            "approximate_presence_count": request.json()["approximate_presence_count"]
        }
    except Exception as e:
        print(e)
        return members
    
    time.sleep(1)
    return members

def enrich_collection_data():
    df = pd.read_csv("data/initial_parse.csv")
    df['Discord Total Members'] = ""
    df['Discord Online Members'] = ""
    
    #iterate over Discord column
    for index, row in df.iterrows():
        print("Index: " + str(index) + " of " + str(len(df)))
        print("Name: " + row['Collection'])
        discord_url = row["Discord"]
        try:
            discord_members = get_guild_members(discord_url)
            df.loc[index, 'Discord Total Members'] = discord_members["approximate_member_count"]
            df.loc[index, 'Discord Online Members'] = discord_members["approximate_presence_count"]
        except:
            df.loc[index, 'Discord Total Members'] = "N/A"
            df.loc[index, 'Discord Online Members'] = "N/A"
        
        print("Total Members: " + str(df.loc[index, 'Discord Total Members']))
        print("Online Members: " + str(df.loc[index, 'Discord Online Members']))
        print("--------------------------------------------------")
    
    df.to_csv('data/parsed_discord_members.csv', index=False)
        
            
    


    