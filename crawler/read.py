from zhihu_oauth import ZhihuClient
from zhihu_oauth import *
import time
import random
import pandas as pd
import os
import csv
from datetime import datetime
import time
from pymongo import MongoClient
import json
from utils import Cleaner

TOKEN_FILE="token.pkl"
client = ZhihuClient()
if os.path.isfile(TOKEN_FILE):
    client.load_token(TOKEN_FILE)
else:
    client.login_in_terminal()
    client.save_token(TOKEN_FILE)
client.save_token('token.pkl')

question_id = 294220610
topic_id = 19575211

topic = client.topic(topic_id)
#print("topic {} has {} questions\n".format(topic.name, topic.questions_count))
#print("topic {} has {} followers\n".format(topic.name, topic.followers_count))


# for act in topic.activities:
#     if(isinstance(act, Answer)):
#         print("this answer content is {}\n".format(act.content))
#
#     else:
#         assert(isinstance(act, Question))
#         print("this question name is {}\n".format(act.title))

topics_list_ = [19575211]
me = client.me
index = 0
topic_questions_detail = []


#df = pd.DataFrame(topic_questions_detail,columns=['tid','qid','aids'])

mogo_client = MongoClient('mongodb://localhost:27017/')
db = mogo_client['test']
col = db['questions_detail']

print(col.count())
#target = col.find_one({'tid' : 19575211 })
target = pd.DataFrame(list(col.find()))
#print(target.describe())
print(target)
for answers in target['aids']:
    for ans_id in answers:
        ans = client.answer(ans_id)
        print(Cleaner.filter_tags(ans.content))
        time.sleep(3)




# for q in topic.unanswered_questions:
#     if(q.follower_count > 1000):
#         #print("question {}, created at {}, has {} followers, {} answers\n".format(q.title, datetime.utcfromtimestamp(q.created_time).strftime('%Y-%m-%d %H:%M:%S'), q.follower_count, q.answer_count))
#         for ans in q.answers:
#             for com in ans.comments:
#                 print("question {} - answer {} {}- comments {}\n".format(q.id, ans.id, ans.content, com.content))




#TODO: filter out unnecessary words or tags

# with open("record.csv",'w',encoding='gbk') as f:
#     w = csv.DictWriter(f,rows[0].keys())
#     w.writerows(rows)