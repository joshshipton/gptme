import numpy as np
import pandas as pd
import sqlite3
import os
import json
import datetime
import re

folder_path = 'C:\\Users\\Shipt\\Desktop\\chatbot\\data\\messages\\inbox'
db = sqlite3.connect('database.db')
cursor = db.cursor()
data = {'text': [], 'handle_id': [], 'is_from_me': [], 'date': []}


for root, dirs, files in os.walk(folder_path):
    for dir in dirs:
        # Get a list of all the JSON files in the subdirectory
        json_files = [f for f in os.listdir(
            os.path.join(root, dir)) if f.endswith('.json')]

        # Loop through the JSON files
        for json_file in json_files:
            with open(os.path.join(root, dir, json_file), 'r', encoding='iso-8859-1') as f:
                json_data = f.read().encode('utf-8').decode('utf-8-sig')
                json_data = json.loads(json_data)

        # Check that its not a gc cause thats too hard rn #imdumb #defeated
            if len(json_data['participants']) != 2:
                continue

         # Extract the required data from the JSON object
            messages = json_data['messages']

          # Do something with the data
            for message in messages:
                try:
                    # removes emojis
                    content = re.sub(r'[^\x00-\x7F]+', '', message['content'])
                    data['text'].append(content)
                    # uses binary to flag if was sent by me or not
                    who_from = (message['sender_name'])
                    if who_from == 'Josh Shipton' or who_from == 'joshshipo':
                        data['is_from_me'].append(1)
                    else:
                        data['is_from_me'].append(0)

                    data['handle_id'].append(who_from)

                    # converts the weird timestamp fb gives into normal data
                    timestamp_ms = message['timestamp_ms']
                    date_time = datetime.datetime.fromtimestamp(
                        timestamp_ms/1000.0)
                    data['date'].append(date_time)

                except (KeyError):
                    continue


df = pd.DataFrame(data)
# making masks to fix data 
mask = (df['text'].str.lower().str.split().str[1] == 'reacted') | (
    df['text'].str.lower().str.split().str[0] == 'reacted')
df = df.loc[~mask]
mask = df['text'].str.contains('Liked a message')
df = df.loc[~mask]

# testing code
file_path = 'new_file.txt'
with open(file_path, 'a', encoding='utf-8') as f:
    f.write(df.to_csv(header=False, index=False))


df.dropna(subset=['text'], inplace=True)


def make_sentences(series):
    return '. '.join(series)


train_data = pd.DataFrame(columns=['text', 'response'])

# iterate thru each convo
for person in pd.unique(df['handle_id']):
    conversation = df[df['handle_id'] == person]
    grouped = (conversation.groupby(conversation.is_from_me.diff().ne(0).cumsum(), as_index=False)
               .agg({'text': make_sentences, 'is_from_me': 'first',
                     'handle_id': 'first', 'date': 'first'}))
    tmp = pd.DataFrame({'text': list(conversation['text'][0:-1]),
                        'response': list(conversation['text'][1:])})

    train_data = pd.concat(
        [train_data, tmp[['text', 'response']]], ignore_index=True)

# make lowercase
train_data['text'] = train_data['text'].apply(lambda x: x.lower())
train_data['response'] = train_data['response'].apply(lambda x: x.lower())

train_data.to_sql('chatbot', db, if_exists='replace', index=False)

# Read the data from the database to confirm that it was written correctly
df = pd.read_sql_query('SELECT * FROM chatbot', db)
#print(df.head())
print('doneski')
