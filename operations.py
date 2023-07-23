import json
import os

import pinecone
from dotenv import find_dotenv, load_dotenv


class PineconeOperations:

    def __init__(self):
        _ = load_dotenv(find_dotenv())  # read local .env file
        api_key = os.getenv('PINECONE_KEY')
        api_env = os.getenv('PINECONE_ENVIRONMENT')

        pinecone.init(
            api_key=api_key,
            environment=api_env
        )
        self.index = None

    def create_index(self, index_name='default') -> list:
        # fetch the list of indexes
        indexes = pinecone.list_indexes()

        # create index if there are no indexes found
        if len(indexes) == 0:
           pinecone.create_index(index_name, dimension=4)


        return indexes

    def connect_index(self):
        indexes = self.create_index()
        # connect to a specific index
        self.index = pinecone.Index(indexes[0])

    def upsert(self, data):
        res = self.index.upsert(vectors=data, namespace="quickstart")        
        return json.loads(str(res).replace("'", '"'))        

    def query(self, query_vector):
        response = self.index.query(
            vector=query_vector,
            top_k=2,
            include_values=True,
            namespace="quickstart"
        )
        return json.loads(str(response).replace("'", '"'))
    
    
