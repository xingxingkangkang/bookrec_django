import random

import DoubanData.tools as tool
import numpy as np
import pandas as pd

tags = tool.read("..//DoubanData//tags.txt")


def combine():
    """
    将所有标签下的书籍整合到一个文件中
    :return:
    """
    books = []
    for tag in tags:
        path = "..//DoubanData//books//" + tag + ".txt"
        one_tag = tool.read(path)
        for one in one_tag:
            books.append(one)
    for book in books:
        tool.write("data//all.txt", book)


def transform():
    """
    将txt文件转换成csv文件，在每个标签下随机取200条数据，若那个标签里的数据不足200条则全取
    :return:
    """
    tool.truncatefile("test.csv")
    name = ['click', 'name', 'author', 'img', 'price', 'publish_time', 'score', 'judge', 'rec_most', 'rec_more',
            'rec_normal', 'rec_bad', 'rec_morebad', 'readed', 'reading', 'readup', 'mess', 'tag']
    data = []
    for tag in tags:
        path = "..//DoubanData//books//" + tag + ".txt"
        one_tag = tool.read(path)
        needed = 200
        if len(one_tag) < needed:
            needed = len(one_tag)
        books = random.sample(one_tag, needed)
        for book in books:
            clicked = 0
            one = book.split(',')
            if float(one[5]) > 9.5 and int(one[6]) > 1000:
                clicked = 1
            if int(one[6]) > 100000:
                clicked = 1
            if float(one[5]) > 7 and int(one[6]) > 1000:
                clicked = 1
            if clicked == 0:
                rd = random.randint(0, 15)
                if rd > 10:
                    clicked = 1
            else:
                rd = random.randint(0, 15)
                if rd > 10:
                    clicked = 0
            data.append([clicked, one[0], one[1], one[2], one[3], one[4], one[5], one[6],
                         one[7], one[8], one[9], one[10], one[11], one[12], one[13],
                         one[14], one[15], one[16]])
    test = pd.DataFrame(columns=name, data=data)
    test.to_csv("test.csv", index=None)


def feature_transform():
    tool.truncatefile("train.csv")
    df1 = pd.read_csv("test.csv")
    df2 = df1.drop(labels=['name', 'author', 'img', 'publish_time', 'mess', 'tag'], axis=1)
    df2.to_csv("train.csv", index=None)


transform()
feature_transform()

