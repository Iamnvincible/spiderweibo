#-*- coding：utf-8 -*-
import requests
import json


def getuserinfo(session, userid):
    USERINFOURL = 'https://m.weibo.cn/api/container/getIndex?type=uid&value=%(id)s&containerid=100505%(id)s' % {
        'id': userid}
    r = session.get(USERINFOURL)
   # print(r.content)
    info = json.loads(r.content.decode('utf-8'))
    return info['data']['userInfo']
