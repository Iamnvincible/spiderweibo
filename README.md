# spiderweibo

这是一个爬取某一个微博用户所发布微博的python程序，
程序会把目标用户的微博写入一个Markdown文件，
微博配图也会下载到文件夹中

## Requirements

PyQuery、BeautifulSoup、request、PIL(Pillow)

## How

在main.py中填写目标用户的微博名称以及要爬取的页数
一页有10条微博
可以控制是否下载大图以及是否下载用户转发的内容

运行python main.py
会提示输入用户名密码，如果登录成功，下次登录不必再次输入凭据

## License

MIT许可证