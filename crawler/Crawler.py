from zhihu_oauth import ZhihuClient
import os
import csv

TOKEN_FILE="token.pkl"

class Crawler:
    client_ = ZhihuClient()
    topic_list_ = [] #监控的话题列表

    def __init__(self,topic_list):
        self.topic_list_ = topic_list
    
        if os.path.isfile(TOKEN_FILE):
            self.client_.load_token(TOKEN_FILE)
        else:
            self.client_.login_in_terminal()
            self.client_.save_token(TOKEN_FILE)

        self.client_.save_token('token.pkl')



