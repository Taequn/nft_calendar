import subprocess
import os
import shutil
import pandas as pd

class TwitterParser:
    def get_name(self):
        return "twitter"
    
    def parse(self, filename=None):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        
        if filename is None:
            filename = "parsed_discord_members"
        
        self.__run_twitter_parser(script_dir)
        # Define the original and destination file paths
        original_file_path = os.path.join(script_dir, 'file.csv')
        destination_file_path = os.path.join(script_dir, '../../data/twitter_data.csv')

        # Copy the original file to the destination with a new name
        shutil.copy(original_file_path, destination_file_path)

    def __run_twitter_parser(self, script_dir):
        # Construct the absolute path to main.go
        main_go_path = os.path.join(script_dir, 'main.go')

        # Run the command in the directory where main.go is located
        subprocess.call(["go", "run", main_go_path], cwd=script_dir)
        
        