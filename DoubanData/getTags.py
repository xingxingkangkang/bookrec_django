from fake_useragent import UserAgent
import os
import re
import time
import requests
import DoubanData.tools as tools


location = os.getcwd() + '/fake_useragent.json'
ua = UserAgent(path=location)
start = time.time()


def getheaders():
    """
    通过fake_useragent来生成一个请求头，反反爬虫的一种措施
    :return: 每次随机返回一个请求头
    """
    user_agent = ua.random
    headers = {'User-Agent': user_agent}
    return headers


def get_tags():
    head = getheaders()
    url = "https://book.douban.com/tag/?view=type&icn=index-sorttags-all"
    while True:
        try:
            data = requests.get(url, headers=head, timeout=10).text
            pat = '<td><a href="/tag/.*?">(.*?)</a>'
            pattern = re.compile(pat)
            return pattern.findall(data)
        except Exception as e:
            print(e)


def get_book_url(name, path):
    """
    获取每本书的URL
    :param name: 传入的每个标签
    :return: 返回每个标签所对应的20*50本书的url
    """
    for i in range(0, 50):
        url = "https://book.douban.com/tag/" + name + "?start=" + str(i * 20) + "&type=T"
        print(url)
        head = getheaders()
        while True:
            try:
                req = requests.get(url, headers=head, timeout=10)
                print(req.status_code)
                data = req.text
                pat = '<a href="(.*?)" title=".*?"'
                pattern = re.compile(pat)
                books_url = pattern.findall(data)
                print("Len:")
                print(len(books_url))
                for urls in books_url:
                    print(urls)
                    tools.write(path, urls)
                break
            except Exception as e:
                print(e)


tags = get_tags()
print(tags)
# for tag in tags:
#     tools.write("tags.txt", tag)

for tag in tags:
    path = "urls//" + tag + ".txt"
    get_book_url(tag, path)

