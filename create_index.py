from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
import sqlite3
from cleandata import train_data

conn = sqlite3.connect('database.db')
index_name = 'chatbot_data'
es = Elasticsearch(['http://localhost:9200/'])

# query = 'SELECT text, response FROM chatbot'

# # Execute the query and fetch the data
# cursor = conn.execute(query)
# rows = cursor.fetchall()

# data = []

# # Iterate over the rows and add them to the list
# for row in rows:
#     doc = {
#         'text': row[0],
#         'response': row[1],
#     }
#     data.append(doc)

# # Use the Elasticsearch bulk API to index the data
# bulk(es, data, index=index_name, raise_on_error=True)

texts_dict = train_data.to_dict(orient='records')
bulk(es, texts_dict, index='textbot', raise_on_error=True)
