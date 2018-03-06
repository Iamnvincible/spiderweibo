#-*- coding：utf-8 -*-
from login import login
from getcards import get_cards,parser_cards,getaccuracytime
import savecard
import getuser
session=login()
#要获取的微博用户的用户名，如果有多个在其后添加
usernames=['爱可可-爱生活']
#选择一个要下载的用户
username=usernames[0]
usernameurl='https://m.weibo.cn/n/'
combined=usernameurl+username
r=session.get(combined)
if r.url==combined:
    print("用户不存在")
else:
    uid=r.url[21:]
    info=getuser.getuserinfo(session,uid)
    count=info['statuses_count']
    print('user has posted %d status'%(count))
    cards=[]
    #range指定要下载的页数，一页一般为10条
    for i in range(1):
        rawcards=get_cards(session,uid,i+1)
        card=parser_cards(session,rawcards,0)
        cards.extend(card)
    print('saving data...')
    #保存到markdown
    savecard.savetomd(cards,1)
    print('done!')
    