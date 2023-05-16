import requests
import time
import pandas as pd

class DiscordParser:
    def get_name(self):
        return "discord"
    
    def parse(self, filename=None, save=False):
        if filename is None:
            filename = "parsed_discord_members"
        
        data = self.__discord_parse()
        if save:
            data.to_csv(f"data/{filename}.csv", index=False)
        
        return data
    
    def __get_guild_members(self, inite_link):
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

    def __discord_parse(self, filename='initial_parse'):
        df = pd.read_csv(f'data/{filename}.csv')
        df['Discord Total Members'] = ""
        df['Discord Online Members'] = ""
        
        #iterate over Discord column
        for index, row in df.iterrows():
            print("Index: " + str(index) + " of " + str(len(df)))
            print("Name: " + row['Collection'])
            discord_url = row["Discord"]
            try:
                discord_members = self.__get_guild_members(discord_url)
                df.loc[index, 'Discord Total Members'] = discord_members["approximate_member_count"]
                df.loc[index, 'Discord Online Members'] = discord_members["approximate_presence_count"]
            except:
                df.loc[index, 'Discord Total Members'] = "N/A"
                df.loc[index, 'Discord Online Members'] = "N/A"
            
            print("Total Members: " + str(df.loc[index, 'Discord Total Members']))
            print("Online Members: " + str(df.loc[index, 'Discord Online Members']))
            print("--------------------------------------------------")
        
        return df
        
            
    


    