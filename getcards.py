#-*- coding：utf-8 -*-
import requests
import json
from pyquery import PyQuery
from bs4 import BeautifulSoup
import re
import time


def get_cards(session, userid, page):
    print("request weibo...")
    resp = session.get(
        'https://m.weibo.cn/api/container/getIndex?type=uid&value=%(targetuser)s&containerid=107603%(targetuser)s&page=%(page)d' % {'targetuser': userid, 'page': page})
    jobject = json.loads(resp.content.decode('utf-8'))
    print("got data!")
    return jobject['data']['cards']

#解析内容，retweeted=1为获取转发内容
def parser_cards(session, data: list, retweeted=0):
    POST_PATH = 'https://m.weibo.cn/statuses/extend?id={0}'
    cards = []
    for card in data:
        if 'mblog' not in card:
            continue
        if 'retweeted_status' in card['mblog'] and retweeted == 0:
            continue
        status = []
        pics = []
        # print(card['mblog']['created_at'])
        accuracytime = getaccuracytime(session, card)
        #可以在此筛选时间
        # t = time.strptime(accuracytime, "%Y-%m-%d %H:%M:%S %A")
        # f = time.strptime('2018-02-14', "%Y-%m-%d")
        # if t.tm_year == f.tm_year and t.tm_mon == t.tm_mon and t.tm_mday == f.tm_mday:
        # if t>f:
        id = card['mblog']['id']
        if 'pics' in card['mblog']:
            largepics = []
            smallpics = []
            for pic in card['mblog']['pics']:
                smallpics.append(pic['url'])
                largepics.append(pic['large']['url'])
            pics.append(smallpics)
            pics.append(largepics)
        if is_short_text(card['mblog']['text']):
            status.append(get_text(card['mblog']))
        else:
            t = get_post_url_json(session, t_url=POST_PATH.format(id))
            status.append(get_text(t['data']))
        if retweeted == 1:
            if 'retweeted_status' in card['mblog']:
                jsontext = json.dumps(card['mblog']['retweeted_status'])
                jsontext = '{\"mblog\":'+jsontext+'}'
                jsonobj = json.loads(jsontext)
                recard = parser_cards(session, [jsonobj])
                if len(recard[0][1]) > 0:
                    pics.append(recard[0][1][0])
                    pics.append(recard[0][1][1])
                status[0] = status[0]+"\n转发:\n"+recard[0][0]
        status.append(pics)
        status.append(id)
        status.append(accuracytime)
        cards.append(status)

    return cards


def is_short_text(data: str):
    if PyQuery(data).find('a:contains(全文)'):
        return False
    else:
        return True


def get_text(data):
    if data:
        if 'longTextContent' in data:
            return clear_html(data['longTextContent'])
        else:
            return clear_html(data['text'])


def clear_html(data: str):
    context = PyQuery(data)
    if context('a').attr('href') != None:
        # links=context('a').map(lambda i,e:PyQuery(e).attr('href'))
        for item in context('a').items():
            x = item.attr('href')
            y = item.text()
            item.text(' ['+y+']'+'('+x+')')
        return context.text()
        # text=""
        # for link in links:
        #     text=text+' '+link
        # return  context.text()+text
        # for index in range(context('a').length):
        #     context('a')[i].attrib[]
        #     context('a').map(lambda i,e:PyQuery(e).text(context('a').map(lambda i,e:PyQuery(e).attr('href'))[index])
    else:
        return context.text()


def get_post_url_json(session, t_url=None):
    # _sleep()
    #c_resp = c_url and session.get(c_url).json()
    t_resp = t_url and session.get(t_url).json()
    return t_resp


def getaccuracytime(session, card):
    if 'scheme' in card:
        r = session.get(card['scheme'])
        soup = BeautifulSoup(r.content, 'html.parser')
        scripts = soup.find_all('script')[1]
        text = scripts.text
        p = '{\s{5}\"status"[\s\S]*\n\}'
        m = re.compile(p)
        result = m.findall(text)
        card = json.loads(result[0])
        return processtime(card['status']['created_at'])
    else:
        return None


def processtime(t):
    t = t.replace(' +0800', '')
    x = time.strptime(t, "%a %b %d %H:%M:%S %Y")
    return time.strftime("%Y-%m-%d %H:%M:%S %A", x)
