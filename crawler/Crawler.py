from zhihu_oauth import ZhihuClient
import os
import csv
import numpy as np
import pandas as pd
from utils import mongo
from pymongo import MongoClient
import random
import time
from utils import Cleaner
import re
import urllib
import numpy as np
import requests
DB_NAME = 'test'
TOKEN_FILE="token.pkl"
TOPICS_COLLECTION = 'questions_detail' #每条record存着tid-qid-aids
ANSWERS_COLLECTION = 'answers_detail' #每条record存着aid-回答内容
MAX_QUESTIONS_PER_TOPIC = 100 #每个话题最多爬取的问题数量，从最新的往旧的问题爬取

class Crawler:
    client_ = ZhihuClient()
    topic_question_df = pd.DataFrame()
    topics_list_ = [19610354,20010203] #监控的话题列表
    questions_detail_ = {} #每个问题的问题标题，问题内容，关注人数，回答人数，回答内容，评论内容，包含话题
    answers_persisted = set()
    answers_to_download = []
    def __init__(self,topics_list=[]):
        if(len(topics_list) > 0):
            self.topic_lists_ = topics_list

        if os.path.isfile(TOKEN_FILE):
            self.client_.load_token(TOKEN_FILE)
        else:
            self.client_.login_in_terminal()
            self.client_.save_token(TOKEN_FILE)

        self.client_.save_token('token.pkl')
        self.db_ = MongoClient(host="localhost", port=27017)[DB_NAME]




    def get_topics_detail(self):

        '''
        dataframe format

        [topic_id, question_id, answer_id_list]

        :return:
        '''
        #old_topics_detail = pd.DataFrame(list(self.db_[TOPICS_COLLECTION].find()))
        #print(old_topics_detail)
        for topic_id in self.topics_list_:
            count = 0
            topic = self.client_.topic(topic_id)
            for q in topic.unanswered_questions:
                if(count > 0):
                    break
                answers = [ans.id for ans in q.answers]
                if(len(answers) > 10):#只记录有人回答的问题id，减少储存量
                    for ans_id in answers:
                        self.answers_to_download.append(ans_id)
                    count += 1
                    print(len(self.answers_to_download))
                    # new_record = {
                    #     'tid' : topic_id,
                    #     'qid' : q.id,
                    #     'aids' : answers
                    #
                    # }
                    # if(len(old_topics_detail[(old_topics_detail['tid'] == topic_id) & (old_topics_detail['qid'] == q.id)]) > 0):
                    #     self.db_[TOPICS_COLLECTION].update_one({'tid': topic_id, 'qid': q.id}, {'$set': new_record})
                    #     print("update {}".format(new_record))
                    # else:
                    #     self.db_[TOPICS_COLLECTION].insert_one(new_record)
                    #     print("insert {}".format(new_record))
                #TODO-some rest function here
                if(random.randint(0,100) % 10 == 0):
                    time.sleep(random.randint(1,3))
                    print("sleep done")

        arr = np.array(self.answers_to_download)
        np.save("answers_to_download.npy",arr)
        #TODO-find out how to update this list

    def get_questions_detail(self):#只搜集符合一定条件的问题详细内容，如关注者/回答数量等超过一定值，但本值不应较大
        #如果mongodb中已经存了回答内容，那么也不考虑作者更新回答的情况，因为答案通常较长，IO成本较高
        all_answers_id = pd.DataFrame(list(self.db_[TOPICS_COLLECTION].find()))
        for answers in all_answers_id['aids']:#提取每个问题对应的所有回答id
            for ans_id in answers:

                ans = self.client_.answer(ans_id)
                ans_content = Cleaner.filter_tags(ans.content)
                comment_content = ""
                if(ans.comment_count > 0):
                    for comment in ans.comments:
                        comment_content += Cleaner.filter_tags(comment.content) + "@"#用@分割，以后可以选择直接测情绪也可以每句评论分开测
                time.sleep(random.randint(1,4))
                print("ans {} done retrival and cleaning".format(ans.id))

                ans_detail ={
                    'aid' : ans_id,
                    'votes' : ans.voteup_count,
                    'content' : ans_content,
                    'comments' : comment_content,
                    'author_follower_num' : ans.author.follower_count
                }

                self.db_[ANSWERS_COLLECTION].insert_one(ans_detail)



        #TODO-data cleaning

        #TODO-in what format to save these data

    def parse_img_src(self, html):
        replace_pattern = r'<[img|IMG].*?/>'  # img标签的正则式
        img_url_pattern = r'.+?src="(\S+)"'  # img_url的正则式
        replaced_img_url_list = []
        img_url_list = []
        need_replace_list = re.findall(replace_pattern, html)  # 找到所有的img标签
        for tag in need_replace_list:
            img_url_list.append(re.findall(img_url_pattern, tag)[0])  # 找到所有的img_url
        return img_url_list

    def save_img(self, img_url, file_name, file_path='./images/'):
        # 保存图片到磁盘文件夹 file_path中，默认为当前脚本运行目录下的 book\img文件夹
        try:
            if not os.path.exists(file_path):
                # os.mkdir(file_path)
                os.makedirs(file_path)
            # 获得图片后缀
            #file_suffix = os.path.splitext(img_url)[1]
            # 拼接图片名（包含路径）
            filename = '{}{}{}'.format(file_path, os.sep, file_name)
            # 下载图片，并保存到文件夹中
            img = requests.get(img_url)
            with open(filename,"wb") as f:
                f.write(img.content)
        except IOError as e:
            print("error")
        except Exception as e:
            print("error")
    def download_images(self, path):
        '''
            answers_to_download里回答的images下载存下来
        :return:
        '''
        for ans_id in self.answers_to_download:
            answer = self.client_.answer(ans_id)
            content = answer.content
            img_src_list = self.parse_img_src(content)
            print("img src list : {}".format(img_src_list))
            for img_url in img_src_list:
                self.save_img(img_url,img_url[-10:],"./images")
                print("picture {} download complete".format(img_url))
            print("answer {} download complete".format(ans_id))




crawl = Crawler()
crawl.get_topics_detail()
crawl.download_images("./images/")
