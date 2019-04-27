import pandas as pd
from zhihu_oauth import ZhihuClient
client = ZhihuClient()
from zhihu_oauth.exception import NeedCaptchaException

try:
    client.login('1026193951@qq.com', 'justbemyself1998')
except NeedCaptchaException:
    # 保存验证码并提示输入，重新登录
    with open('a.gif', 'wb') as f:
        f.write(client.get_captcha())
    captcha = input('please input captcha:')
    client.login('1026193951@qq.com', 'justbemyself1998',captcha)
    client.save_token("token.pkl")