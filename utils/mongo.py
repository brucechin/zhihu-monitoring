import sys
import pandas as pd
import json
from pymongo import MongoClient
import sys
import pandas as pd
import json
from pymongo import MongoClient

class MongoBase:
    def __init__(self, db):
        self.client_ = MongoClient(host="localhost", port=27017)
        self.db_ = self.client_[db]

    def get(self, collection, key):
        #查询结果返回为dataframe格式
        col = self.db_[collection]
        res = pd.DataFrame(list(col.find(key)))
        return res

    def insert_many(self, collection, input):
        col = self.db_[collection]
        col.insert_many(input)

