# 💻 ChatBot Data Preprocessing
This folder contains a script that preprocesses Facebook Messenger and Instagram direct message data to create training data. The script then creates an index in Elastic search to store the chatbot data. It then uses the Elasticseach index to retrieve responses to user messages using [TF-IDF](https://en.wikipedia.org/wiki/Tf%E2%80%93idf) The data can be downloaded [here](https://www.facebook.com/help/212802592074644).

### 📝 Prerequisites
###### To use this script, you'll need:
Python 3.6 or later
NumPy
Pandas
SQLite3

