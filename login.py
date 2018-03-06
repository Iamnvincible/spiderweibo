from os import path
import requests
import pickle
from pyquery import PyQuery

#主登录函数
def login():
    session = loadsession()
    if session == None:
        username=input("Your Username:")
        password=input("Your Password:")
        session = login_wb(username, password)
        return session
    else:
        if need_to_login(session):
            session = login_wb(username, password)
            return session
        else:
            return session

#载入已经保存的session
def loadsession():
    if path.exists('session'):
        with open('session', 'rb') as fr:
            session = pickle.load(fr)
            print('load session from cache')
            return session
    else:
        return None

#判断session过期需要重新登录
def need_to_login(session):
    resp = session.get('https://m.weibo.cn')
    if 'passport' in resp.url or 'login' in resp.url:
        print('need to login')
        return True
    else:
        return False

#登录函数
def login_wb(username, password):
    session = requests.session()
    url = 'http://m.weibo.cn'
    post_url = 'https://passport.weibo.cn/sso/login'
    data = {
        'username': username,
        'password': password,
        'savestate': '1',
        'r': 'http://m.weibo.cn/',
        'ec': '0',
        'pagerefer': '',
        'entry': 'mweibo',
        'wentry': '',
        'loginfrom': '',
        'client_id': '',
        'code': '',
        'qq': '',
        'mainpageflag': '1',
        'hff': '',
        'hfp': ''
    }
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.109 Mobile Safari/537.36'
    })
    resp = session.get(url)
    session.headers.update(
        {'Referer': find_referer_url(resp.text)})
    resp = session.post(post_url, data=data)
    if resp.status_code == 200:
        print('signed in')
        with open('session', 'wb') as fw:
            pickle.dump(session, fw)
        return session
    else:
        print('login failed')
        return None


def find_referer_url(text):
    doc = PyQuery(text)
    a_tag = doc.find('.action a').eq(1)
    return a_tag.attr('href')


if __name__ == '__main__':
    login()
