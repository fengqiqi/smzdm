# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2021/11/9
# @Author  : Fitch
# @File    : smzdm_web_sign.py
# @Software: PyCharm

'''
cron:  0 6 * * * smzdm_web_sign.py
new Env('什么值得买web签到');
'''
import requests,os,json,logging

class SMZDM_Bot(object):
    def __init__(self):
        self.session = requests.Session()
        # 添加 headers
        self.session.headers = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Host': 'zhiyou.smzdm.com',
            'Referer': 'https://www.smzdm.com/',
            'Sec-Fetch-Dest': 'script',
            'Sec-Fetch-Mode': 'no-cors',
            'Sec-Fetch-Site': 'same-site',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36',
        }
    """
    对请求 盖乐世社区 返回的数据进行进行检查
    1.判断是否 json 形式
    """
    def __json_check(self, msg):

        try:
            result=msg.json()
            return True
        except Exception as e:
            logging.info(f'Error : {e}')
            return False

    """
    起一个什么值得买的，带cookie的session
    cookie 为浏览器复制来的字符串
    :param cookie: 登录过的社区网站 cookie
    """
    def load_cookie_str(self, cookies):
        self.session.headers['Cookie'] = cookies

    """
    签到函数
    """
    def checkin(self):
        url = 'https://zhiyou.smzdm.com/user/checkin/jsonp_checkin'
        msg = self.session.get(url)
        if self.__json_check(msg):
            return msg.json()
        return msg.content

if __name__ == '__main__':
    sb = SMZDM_Bot()
    with open("./smzdm_cookie.json", "r", encoding='UTF-8') as f:
        datas = f.read()
        datas = json.loads(datas.encode('UTF-8').decode('latin-1'))
    cookie = datas['cookie']
    sb.load_cookie_str(cookie)
    res = sb.checkin()
    if(res['error_code'] != '0'):
        logging.info(res['error_msg'])
    else:
        logging.info('签到执行完毕')
    logging.info('返回信息:', res)
