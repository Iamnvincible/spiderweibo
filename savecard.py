#-*- coding：utf-8 -*-
import requests
import os
import time
import codecs
from PIL import Image

# 将cards中的微博文本内容保存到文本中


def saveutf8txt(cards):
    folder = time.strftime("%Y-%m-%d", time.localtime())
    if not os.path.exists(folder):
        os.mkdir(folder)
    os.chdir(folder)
    for card in cards:
        f = codecs.open(card[2]+".txt", "w", "utf-8")
        f.write(card[0])
        f.close()

# 将cards中的文本和图片保存到markdown文件中，可选参数largepic=1是下载大图


def savetomd(cards, largepic=0):
    folder = time.strftime("%Y-%m-%d", time.localtime())
    if not os.path.exists(folder):
        os.mkdir(folder)
    os.chdir(folder)
    f = codecs.open(folder+".md", "w", "utf-8")
    for card in cards:
        f.write(card[0])
        if len(card[1]) > 0:
            print('downloading picture(s)...')
            if largepic == 1:
                pics = get_pics(card[1][1], card[2])
            else:
                pics = get_pics(card[1][0], card[2])
            print('processing pictures...')
            picname = getIncorporated(pics)
            f.write('\r\n')
            f.write('![图片](%(file)s)' % {'file': picname})
        f.write('\n'+card[3])
        f.write('\n\n---\n')
        f.write('\n\n')
    f.close()

# 下载图片到当前目录，以微博的id为文件名加下划线数字递增


def get_pics(pics, ids):
    filenames = []
    for index, u in enumerate(pics):
        filename = ids+"_"+str(index+1)+u[-4:]
        if os.path.isfile(filename):
            filenames.append(filename)
            continue
        filenames.append(filename)
        r = requests.get(u)
        with open(filename, 'wb') as f:
            f.write(r.content)
    return filenames

# 将多张图片合并成一张图


def Incorparate(squarepics):
    count = len(squarepics)
    sq = 128
    if count <= 1:
        return squarepics[0]
    if count > 1 and count < 4:
        target = Image.new('RGB', (sq*count, sq), '#FFFFFF')
        for i in range(count):
            target.paste(squarepics[i], (i*sq, 0, i*sq+sq, sq))
        return target
    elif count == 4:
        target = Image.new('RGB', (sq*2, sq*2), '#FFFFFF')
        for i in range(2):
            target.paste(squarepics[i], (i*sq, 0, i*sq+sq, sq))
        for j in range(2):
            target.paste(squarepics[j+2], (j*sq, sq, j*sq+sq, 2*sq))
        return target
    else:
        ys = 2
        if count > 6:
            ys = 3
        target = Image.new('RGB', (sq*3, sq*ys), '#FFFFFF')
        row = 0
        col = 0
        for i in range(count):
            target.paste(squarepics[i], (row*sq, col*sq, row*sq+sq, col*sq+sq))
            row = (i+1) % 3
            col = int((i+1)/3)
        return target

# 图片的剪切


def cropimg(filename):
    im = Image.open(filename)
    length, width = im.size
    square = min(length, width)
    if square == length:
        x = 0
        y = int(width/2-square/2)
        region = im.crop((x, y, square, y+square))
    else:
        x = int(length/2-square/2)
        y = 0
        region = im.crop((x, y, x+square, square))
    return region.resize((128, 128), Image.ANTIALIAS)

# 获得剪切合并后的图片


def getIncorporated(picnames):
    if len(picnames) == 1:
        im = Image.open(picnames[0]).convert('RGB')
        x, y = im.size
        if x > 128*3 or y > 128*3:
            w = max(x, y)
            rate = 128*3/w
            im.resize((int(x*rate), int(y*rate)),
                      Image.ANTIALIAS).save(picnames[0], 'JPEG', quality=100)
        return picnames[0]
    else:
        squarefilename = picnames[0][0:-6]+'.jpg'
        if os.path.isfile(squarefilename):
            return squarefilename
        img = []
        for item in picnames:
            img.append(cropimg(item))
        square = Incorparate(img)
        square.save(squarefilename, 'JPEG', quality=100)
        return squarefilename
