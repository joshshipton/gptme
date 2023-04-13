#### 💻 ChatBot Data Preprocessing
This script preprocesses Facebook Messenger data to create a dataset that can be used for training a chatbot.

### 📝 Prerequisites
To use this script, you'll need:

# Python 3.6 or later
NumPy
Pandas
SQLite3
JSON
Datetime
Regular expressions
Itertools
###🚀 Getting Started
Clone this repository to your local machine.
Navigate to the repository folder.
Update the folder_path variable in main.py with the path to the folder containing the Messenger data you want to preprocess.
Run the main.py script using the command python main.py.
📊 Data Preprocessing
The script reads in Facebook Messenger data from JSON files and stores it in a SQLite3 database. It then preprocesses the data to create a clean dataset that can be used to train a chatbot. The preprocessing steps include:

Removing emojis from messages
Flagging messages as sent by the user or received from the other party
Converting timestamps to datetime format
Writing the dataset to a CSV file
###📈 Data Transformation
The script transforms the data into a format suitable for training a chatbot by:

Grouping messages by conversation and sender
Concatenating repeated messages into a single message
Assigning the first message as the "text" and the subsequent message as the "response"
###📄 Output
The script outputs a CSV file containing the preprocessed data. The file can be used to train a chatbot using machine learning algorithms.

###🤖 ChatBot
This script is only for data preprocessing and does not include code for training a chatbot. Once you have preprocessed your data, you can use it to train a chatbot using a machine learning algorithm of your choice.
