import subprocess
import os
import shutil


def run_twitter_parser():
    # Get the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Construct the absolute path to main.go
    main_go_path = os.path.join(script_dir, 'main.go')

    # Run the command in the directory where main.go is located
    subprocess.call(["go", "run", main_go_path], cwd=script_dir)
    
    # Define the original and destination file paths
    original_file_path = os.path.join(script_dir, 'file.csv')
    destination_file_path = os.path.join(script_dir, '../../data/twitter_data.csv')

    # Copy the original file to the destination with a new name
    shutil.copy(original_file_path, destination_file_path)