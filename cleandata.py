import pandas as pd
import sqlite3
import os
import json
path = 'C:\\Users\\Shipt\\Desktop\\chatbot\\data\\messages\\inbox'

for root, dirs, files in os.walk(path):
    for dir in dirs:
        # Get a list of all the JSON files in the subdirectory
        json_files = [f for f in os.listdir(
            os.path.join(root, dir)) if f.endswith('.json')]

        # Loop through the JSON files
        for json_file in json_files:
            with open(os.path.join(root, dir, json_file), 'r') as f:
                json_data = json.load(f)

            # Extract the required data from the JSON object
            participants = json_data['participants']
            messages = json_data['messages']

            # Do something with the data
            for participant in participants:
                print(participant['name'])
            
            for message in messages:
                try:
                    print(message['sender_name'])
                    print(message['content'])
                except(KeyError):
                    continue



