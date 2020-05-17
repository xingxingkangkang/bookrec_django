import DoubanData.tools as tools
from DoubanData.books import Book
import re


tags = tools.read("tags.txt")
# tags = ["test"]


def step_one():
    """
    清洗数据，因为在爬虫的时候会有失败的数据，失败的话我就直接把url写入文件
    失败的记录它长度肯定是小于50的，成功的数据长度都是大于50的
    :return:
    """
    count = 0
    for tag in tags:
        path = "books//" + tag + ".txt"
        old_books = tools.read(path)
        new_books = []
        for old_book in old_books:
            if len(old_book) > 50:
                new_books.append(old_book)
        tools.truncatefile(path)
        for new_book in new_books:
            count += 1
            tools.write(path, new_book)

    print(count)


def step_two():
    """
    如果在爬虫的时候最后一栏不是标签的话，就运行这个函数进行处理，给他最后加上标签
    :return:
    """
    for tag in tags:
        lis = []
        path = "books//" + tag + ".txt"
        urls_list = tools.read(path)
        for url in urls_list:
            out = url.split(',')
            out.append(tag)
            output = ','.join(out)
            lis.append(output)
        tools.truncatefile(path)
        for li in lis:
            tools.write(path, li)


def step_three():
    """
    正常情况下每一本书的有17个特征，那就把特征值不是17的书当作是异常值来处理，这里是直接舍弃
    :return:
    """
    for tag in tags:
        path = "books//" + tag + ".txt"
        urls = tools.read(path)
        out = []
        for url in urls:
            lis = url.split(',')
            if len(lis) == 17:
                out.append(url)
        tools.truncatefile(path)
        for url in out:
            tools.write(path, url)


def step_four():
    """
    对价格进行格式化处理，因为有些价格不是RMB 采取处理方式是只保留书本价格的数字部分 便于存入数据库
    :return:
    """
    for tag in tags:
        path = "books//" + tag + ".txt"
        books = tools.read(path)
        out = []
        for book in books:
            lis = book.split(',')
            price = lis[3]
            # print(re.findall(r"\d+\.?\d*", price))
            try:
                lis[3] = re.findall(r"\d+\.?\d*", price)[0]
                book = ','.join(lis)
                out.append(book)
            except Exception as e:
                print(e, book)
            # lis[6] = int(lis[7]) + int(lis[8]) + int(lis[9]) + int(lis[10]) + int(lis[11])
            # lis[6] = str(lis[6])
        tools.truncatefile(path)
        for book in out:
            tools.write(path, book)


def step_five():
    """
    去重 先把它放入set再放入list简单去重
    :return:
    """
    for tag in tags:
        print(tag)
        path = "books//" + tag + ".txt"
        books = tools.read(path)
        print(len(books))
        books = list(set(books))
        print(len(books))
        tools.truncatefile(path)
        for book in books:
            tools.write(path, book)


def step_six():
    """
    把数据转换成sql语句
    :return:
    """
    for tag in tags:
        path = "books//" + tag + ".txt"
        books = tools.read(path)
        for book in books:
            bk = Book(book)
            tools.write("to_sql//all.sql", bk.to_sql())


def step_seven():
    """
    在插入数据库的时候发现，有些书籍的名字字段过长导致插入失败
    所以在进行转换成sql语句之前应该先进行这个操作 把书名字段长于60的给舍弃掉
    :return:
    """
    for tag in tags:
        new_books = []
        path = "books//" + tag + ".txt"
        books = tools.read(path)
        for book in books:
            lis = book.split(',')
            name = lis[0]
            if len(name) > 60:
                continue
            new_books.append(book)
        tools.truncatefile(path)
        for book in new_books:
            tools.write(path, book)


# for i in range(len(tags)):
#     sql = "INSERT INTO cate values (null ," + str(i) + ",'" + tags[i] + "');"
#     tools.write("to_sql.sql", sql)
# step_one()
i = 0
while i <= 10:
    print(i, (i * 10-i*10 % 10) / 20)
    i = i + 0.1
