# 💻 ChatBot Data Preprocessing
This folder contains a script that preprocesses Facebook Messenger and Instagram direct message data to create training data. The script then creates an index in Elastic search to store the chatbot data. It then uses the Elasticseach index to retrieve responses to user messages using [TF-IDF](https://en.wikipedia.org/wiki/Tf%E2%80%93idf). You can download your own Facebook messenger and instagram dm data [here](https://www.facebook.com/help/212802592074644).

### 📝 Prerequisites
###### To use this script, you'll need:
Python 3.6 or later
NumPy
Pandas
SQLite3
Elastic-search (run the elasticsearch.bat file in cmd before starting the chatbot)

### Why did I make this?

I made this because I was sick of replying to peoples messages and wanted a way to automate the process. The result was lackluster and is not believeable or useable at all. Probably a result of bad code, not enough training data and tf-idf not really taking into account context and other elements of conversation. If i were to try to remake this I would probably just send messages to chatgpt as prompts and output the response.
