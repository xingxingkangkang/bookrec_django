from fake_useragent import UserAgent
import os
import re
import time
import requests
import threading
import queue as Queue


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


class MyThread(threading.Thread):
    def __init__(self, name, Q):
        threading.Thread.__init__(self)
        self.name = name
        self.Q = Q

    def run(self):
        print("Starting: " + self.name)
        while True:
            try:
                # get_book_urls(self.Q)
                get_book_detail(self.Q)
            except Exception as e:
                print(e)
                break
        print("Exiting: " + self.name)


def get_book_urls(Q):
    """
    获取书籍的详细信息
    :param Q: 这是一个线程同步的队列，先进先出，一个url后面跟着它所对应的tag
    :return: 将每个tag下url都添加到对应的文件中
    """
    url = Q.get(timeout=2)
    tags = Q.get(timeout=2)
    code = 404
    while code != 200:
        head = getheaders()
        req = requests.get(url, headers=head, timeout=10)
        if req.status_code == 200:
            code = 200
        elif req.status_code == 403:
            print("IP已经被封，请更换IP")
            continue
        else:
            continue
        data = req.text
        pat = '<a href="(.*?)" title=".*?"'
        pattern = re.compile(pat)
        books_url = pattern.findall(data)
        # print(books_url)
        if len(books_url) != 0:
            path = "urls//" + tags + ".txt"
            with open(path, 'a+', encoding='UTF-8') as f:
                for urls in books_url:
                    f.write(urls)
                    f.write('\n')


def get_book_detail(Q):
    """
    获取书籍的详细信息
    :param Q:
    :return:
    """
    url = Q.get(timeout=2)
    tag = Q.get(timeout=2)
    code = 404
    while code != 200:
        head = getheaders()
        req = requests.get(url, headers=head, timeout=20)
        new_url = url + "collections"
        new_req = requests.get(new_url, headers=head, timeout=20)
        if req.status_code == 200 and new_req.status_code == 200:
            code = 200
        else:
            continue
        print(url + "响应成功" + tag)
        out = []
        data = req.text
        name_pat = 'title="点击看大图" alt="(.*?)"'
        name_list = re.compile(name_pat, re.S).findall(data)
        if is_none(name_list):
            print("name is null")
            continue
        name = name_list[0]
        out.append(name)

        author_pat = ' <a href="https://book.douban.com/author/.*?">(.*?)</a>'
        author_pat = re.compile(author_pat, re.S)
        author_list = author_pat.findall(data)
        if is_none(author_list):
            author_pat = '<a class="" href="/search.*?>(.*?)</a>'
            pattern = re.compile(author_pat)
            author_list = pattern.findall(data)
        if is_none(author_list):
            print("author is null")
            continue
        author = author_list[0].replace("\n", "").replace(" ", "")
        out.append(author)

        img_src_pat = '<img src="(.*?)" title="点击看大图"'
        img_src_list = re.compile(img_src_pat).findall(data)
        if is_none(img_src_list):
            print("img is null")
            continue
        img_src = img_src_list[0]
        out.append(img_src)

        price_pat = '<span class="pl">定价:</span> (.*?)元?<br/>'
        price_list = re.compile(price_pat).findall(data)
        if is_none(price_list):
            print("price is null")
            continue
        price = price_list[0]
        out.append(price)

        publish_year_pat = '<span class="pl">出版年:</span> (.*?)<br/>'
        publish_year_list = re.compile(publish_year_pat).findall(data)
        if is_none(publish_year_list):
            print("publish year is null")
            continue
        publish_year = publish_year_list[0]
        out.append(publish_year)

        score_pat = '<strong class="ll rating_num.*?> (.*?) </strong>'
        score_list = re.compile(score_pat).findall(data)
        if is_none(score_list):
            print("score is null")
            continue
        score = score_list[0]
        out.append(score)

        rating_people_pat = '<span property="v:votes">(.*?)</span>人评价</a>'
        rating_people_list = re.compile(rating_people_pat).findall(data)  # 评价人数
        if is_none(rating_people_list):
            print("rating people is null")
            continue
        rating_people = rating_people_list[0]
        out.append(rating_people)

        rating_per_pat = '<span class="rating_per">(.*?)%</span>'
        rating_per_list = re.compile(rating_per_pat).findall(data)
        if is_none(rating_people_list):
            print("rating pre is null")
            continue
        for i in range(0, len(rating_per_list)):
            rating_per_list[i] = str(max(int(float(rating_per_list[i]) / 100 * int(rating_people)), 1))
            out.append(rating_per_list[i])

        new_data = new_req.text
        readed_pat = '>(.*?)人读过<'
        readed_list = re.compile(readed_pat).findall(new_data)
        if is_none(readed_list):
            print("readed is null")
        readed = readed_list[0]
        out.append(readed)

        reading_pat = '>(.*?)人在读<'
        reading_list = re.compile(reading_pat).findall(new_data)
        reading = reading_list[0]
        out.append(reading)

        readup_pat = '>(.*?)人想读<'
        readup_list = re.compile(readup_pat).findall(new_data)
        readup = readup_list[0]
        out.append(readup)
        out.append(url)
        out.append(tag)

        output = ','.join(out)
        print(output)
        path_name = "books//" + tag + ".txt"
        with open(path_name, 'a+', encoding='utf-8') as file:
            file.writelines(output)
            file.write('\n')


def is_none(value):
    if len(value) == 0:
        return True
    else:
        return False


threadList = []
workQueue = Queue.Queue(500000)
threads = []
link_list = []
tags = []

for i in range(60):
    thread_name = 'Thread--' + str(i)
    threadList.append(thread_name)

with open("tags.txt", 'r', encoding='UTF-8') as f:
    tags_list = f.readlines()
    for tag in tags_list:
        tag = tag.replace('\n', '')
        tags.append(tag)

for tag in tags:
    path = "urls//" + tag + ".txt"
    with open(path, 'r', encoding='UTF-8') as f:
        urls_list = f.readlines()
        for url in urls_list:
            url = url.replace('\n', '')
            workQueue.put(url)
            workQueue.put(tag)

print(workQueue.qsize())


for tName in threadList:
    thread = MyThread(tName, workQueue)
    thread.start()
    threads.append(thread)

for url in link_list:
    workQueue.put(url)

for t in threads:
    t.join()

end = time.time()

print(end-start)

