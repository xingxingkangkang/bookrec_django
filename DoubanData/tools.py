def write(path, text):
    """
    将数据进入文件
    :param path: 文件路径
    :param text: 写入的内容
    :return:
    """
    with open(path, 'a', encoding='utf-8') as f:
        f.writelines(text)
        f.write('\n')


def truncatefile(path):
    """
    清空指定路径下的文件内容
    :param path:
    :return:
    """
    with open(path, 'w', encoding='utf-8') as f:
        f.truncate()


def read(path):
    """
    读取文件中的内容
    :param path:
    :return: 将文件中的内容一行一行的读取，返回一个列表，每一行对应列表中的一个元素
    """
    with open(path, 'r', encoding='utf-8') as f:
        txt = []
        for s in f.readlines():
            txt.append(s.strip())
    return txt


def gettimediff(start, end):
    """
    计算两个时间节点的时间差
    :param start: 开始节点
    :param end: 结束节点
    :return:
    """
    seconds = (end - start).seconds
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    diff = ("%02d:%02d:%02d" % (h, m, s))
    return diff
