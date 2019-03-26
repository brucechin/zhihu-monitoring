from zhihu_oauth import ZhihuClient
import time
import random
import pandas as pd
import os
import csv

TOKEN_FILE="token.pkl"
client = ZhihuClient()
if os.path.isfile(TOKEN_FILE):
    client.load_token(TOKEN_FILE)
else:
    client.login_in_terminal()
    client.save_token(TOKEN_FILE)
client.save_token('token.pkl')

question_id = 294220610

question = client.question(question_id)
answers = question.answers

rows = []
index = 1
for ans in answers:
    if index <= 10:#question.answer_count:
        rows.append(ans.content)
        index += 1


#TODO: filter out unnecessary words or tags

with open("record.csv",'w',encoding='gbk') as f:
    w = csv.DictWriter(f,rows[0].keys())
    w.writerows(rows)