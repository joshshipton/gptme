from random import randint
from Elasticsearch import es 

randomness = 1
def chatbot():
    quit=False
    while quit== False:
        text = str(input('Me: '))
        ##an optional quit command
        if text == 'quit()':
            quit=True
        else:
            response = es.search(index='textbot', body={ "query": {
                "match": {
                    "text":text
                }
            }})
            try:
                ##introduce a bit of randomness into the response 
                i = randint(0,randomness)
                print("Chabot: %s" % response['hits']['hits'][i]['_source']['response'])
            except:
                print("Chatbot: idk")

chatbot()