import numpy as np
import pandas as pd
import sqlite3
import os
import json
import datetime
import re
from itertools import zip_longest
handle_id = 0




folder_path = 'C:\\Users\\Shipt\\Desktop\\chatbot\\data\\messages\\inbox'
db = sqlite3.connect('database.db')
cursor = db.cursor()
data = {'text': [], 'handle_id': [], 'is_from_me': [], 'date': []}
other_participant = ''


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
            partcipants = json_data['participants']

          # Do something with the data

            person = partcipants[0]
            other_participant = person['name']
            handle_id += 1

            for message in messages:
                try:
                    # removes emojis
                    content = re.sub(r'[^\x00-\x7F]+', '', message['content'])
                    data['text'].append(content)
                    # uses binary to flag if it was sent by me or not
                    who_from = (message['sender_name'])
                    if who_from == 'Josh Shipton':
                        data['is_from_me'].append(1)
                    else:
                        data['is_from_me'].append(0)

                    data['handle_id'].append(handle_id)

                    # converts the weird timestamp fb gives into normal data
                    timestamp_ms = message['timestamp_ms']
                    date_time = datetime.datetime.fromtimestamp(
                        timestamp_ms/1000.0)
                    data['date'].append(date_time)

                except (KeyError):
                    continue


df = pd.DataFrame(data)
file_path = 'output.csv'

# Write the DataFrame to a CSV file
df.to_csv(file_path, index=False)
# making masks to fix data
mask = (df['text'].str.lower().str.split().str[1] == 'reacted') | (
    df['text'].str.lower().str.split().str[0] == 'reacted')
df = df.loc[~mask]
mask = df['text'].str.contains('Liked a message')
df = df.loc[~mask]
df['text'] = df['text'].str.replace('\s+', ' ', regex=True)



df.dropna(subset=['text'], inplace=True)


def make_sentences(series):
    return '. '.join(series)


train_data = pd.DataFrame(columns=['text', 'response'])

# ok
# go through entire dataframes by each individual handleid "meaning the person the conversation is with"
# for each person goes thru and grabs repeated ones with the same is_from_me binary flag
# applies the "make sentences" function to those repeated messages to make them one big message
# then the first message they sent should be "text"
# the next message i sent should be response i and then theirs should be i+1


# iterate thru each convo
for person in pd.unique(df['handle_id']):
    # goes through one person at a time
    conversation = df[df['handle_id'] == person]
    # groups the data by rows when the "is_from_me" changes. applies the "make sentences" function to concate the repeated messages into single sentences

    grouped = (conversation.groupby(conversation.is_from_me.diff().ne(0).cumsum(), as_index=False)
               .agg({'text': make_sentences,
                    'is_from_me': 'first',
                     'handle_id': 'first',
                     'date': 'first',
                     'is_from_me': lambda x: 'from_me' if x.iloc[0] == 1 else 'not_from_me'}))

    sent_messages = grouped[grouped['is_from_me'] == 'from_me']['text'].tolist()
    recv_messages = grouped[grouped['is_from_me'] == 'not_from_me']['text'].tolist()

    # if sent messages are longer then need to skip fist sent message
    # if recieved messages are longer then need to skip last recieved message 
    if len(sent_messages) > len(recv_messages):
        sent_messages = sent_messages[1:]
        # print('sent messages longer, skip the first one')
    elif len(sent_messages) < len(recv_messages):
        recv_messages = recv_messages[:-1]
        # print('recived more messages, skip the last one')

    # # testing code
    # file_path = 'sentt.txt'
    # with open(file_path, 'a', encoding='utf-8') as f:
    #     for message in sent_messages:
    #         f.write(message + '\n')

    # # testing code
    # file_path = 'recv.txt'
    # with open(file_path, 'a', encoding='utf-8') as f:
    #     for message in recv_messages:
    #         f.write(message + '\n')

    tmp = pd.DataFrame({'text': recv_messages,
                        'response': sent_messages})

    train_data = pd.concat(
        [train_data, tmp[['text', 'response']]], ignore_index=True)

# make lowercase
train_data['text'] = train_data['text'].apply(lambda x: x.lower())
train_data['response'] = train_data['response'].apply(lambda x: x.lower())




train_data.to_sql('chatbot', db, if_exists='replace', index=False)

# Read the data from the database to confirm that it was written correctly
df = pd.read_sql_query('SELECT * FROM chatbot', db)
# print(df.head())
print('doneski')


