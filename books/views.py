# coding=utf-8
import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from sklearn.externals import joblib
import numpy as np
from books.models import Book, History
from django.utils import timezone


@csrf_exempt
def getbooks(request):
    """
    这个接口是根据前端传入的tag来返回数据库中对应tag的书籍信息
    请求参数只需要有 tag 就可以
    :param request:
    :return:
    """
    if request.method == "GET":
        books = Book.objects.filter(tag=request.GET.get("tag")).order_by("-judge")
        print("tag=" + request.GET.get("tag"))
        res = dict()
        res['code'] = 200
        res['size'] = books.count()
        res['book_detail'] = dict()
        cnt = 0
        for book in books:
            res['book_detail'][cnt] = dict()
            res['book_detail'][cnt]['id'] = book.id
            res['book_detail'][cnt]['name'] = book.name
            res['book_detail'][cnt]['author'] = book.author
            res['book_detail'][cnt]['img'] = book.img
            res['book_detail'][cnt]['price'] = book.price
            res['book_detail'][cnt]['score'] = book.score
            res['book_detail'][cnt]['publish_time'] = book.publish_time
            res['book_detail'][cnt]['judge'] = book.judge
            res['book_detail'][cnt]['rec_most'] = book.rec_most
            res['book_detail'][cnt]['rec_more'] = book.rec_more
            res['book_detail'][cnt]['rec_normal'] = book.rec_normal
            res['book_detail'][cnt]['rec_bad'] = book.rec_bad
            res['book_detail'][cnt]['rec_morebad'] = book.rec_morebad
            res['book_detail'][cnt]['readed'] = book.readed
            res['book_detail'][cnt]['reading'] = book.reading
            res['book_detail'][cnt]['readup'] = book.readup
            res['book_detail'][cnt]['mess'] = book.mess
            cnt = cnt + 1
        return JsonResponse(data=res)


@csrf_exempt
def getone(request):
    """
    这个接口是根据前端传的某一本书的Id来返回这本书所对应的详细信息
    暂时没有实现对应的前端页面
    请求参数需要包含 id
    :param request:
    :return:
    """
    if request.method == "GET":
        book = Book.objects.filter(id=request.GET.get("id"))[0]
        return JsonResponse({
            "code": 200,
            "data": {
                "id": book.id,
                "name": book.name,
                "author": book.author,
                "img": book.img,
                "price": book.price,
                "publish_lime": book.publish_time,
                "score": book.score,
                "judge": book.judge,
                "rec_most": book.rec_most,
                "rec_more": book.rec_more,
                "rec_normal": book.rec_normal,
                "rec_bad": book.rec_bad,
                "rec_morebad": book.rec_morebad,
                "readed": book.readed,
                "reading": book.reading,
                "readup": book.readup,
                "mess": book.mess,
                "tag": book.tag
            }
        })


@csrf_exempt
def history(request):
    """
    获取用户足迹，只有在当前状态为登录态时才会有数据返回
    POST 表示用户有新的动作需要记录在数据库中
    GET 表示请求用户是点击了历史记录，需要将对应的数据进行返回
    在请求方法中需要包含参数啊 isLogin 和 username
    :param request:
    :return:
    """
    if request.method == 'POST':
        req = json.load(request)
        if req["isLogin"]:
            username = req["username"]
            date = timezone.localtime().strftime("%Y-%m-%d %H:%M:%S")
            action = req["action"]
            bookname = req["bookname"]
            bookid = req["bookid"]
            img = req["img"]
            write_to_history(username, date, action, bookname, bookid, img)
            print("write to database")
            return JsonResponse({
                "code": 200,
                "message": "write to database"
            })
        else:
            print("您还未登录")
            return JsonResponse({
                "code": 400,
                "message": "您还未登录，此次足迹不记录"
            })
    elif request.method == 'GET':
        if request.GET.get("isLogin"):
            name = request.GET.get('username')
            histories = History.objects.filter(name=name).order_by("-time")
            # 用户已经登录，但是之前并未产生足迹
            if len(histories) == 0:
                return JsonResponse({
                    "code": 204,
                    "message": "No data"
                })
            else:
                data = dict()
                cnt = 0
                for recoder in histories:
                    print(recoder.time)
                    data[cnt] = dict()
                    data[cnt]['name'] = recoder.name
                    data[cnt]['date'] = recoder.time
                    data[cnt]['action'] = recoder.action
                    data[cnt]['book'] = recoder.bookname
                    book = Book.objects.filter(id=recoder.bookid)[0]
                    data[cnt]['score'] = book.score
                    i = book.score
                    data[cnt]['show'] = (i * 10-i*10 % 10) / 20
                    data[cnt]['author'] = book.author
                    data[cnt]['judge'] = book.judge
                    cnt = cnt+1
                return JsonResponse({
                    "code": 200,
                    "data": data,
                    "length": cnt
                })
        else:
            # 用户没有登录
            return JsonResponse({
                "code": 400,
                "message": "您还未登录，请先登录后才可以查看"
            })


@csrf_exempt
def like(request):
    """
    返回推荐给用户的书籍，如果是处于未登录态，那我就返回给热门书籍
    如果是在登录态，但是用户并没有历史阅读记录，那我还是返回给热门书籍
    如果是在登录态，并且用户有历史阅读记录了，那我就返回经过推荐算法排序后的书籍
    :param request:
    :return:
    """
    if request.method == "GET":
        isLogin = request.GET.get("isLogin")
        print(isLogin)
        # 如果当前是是未登录的，那我就直接返回评价人数前1000的那些书
        if isLogin == "false":
            books = Book.objects.order_by("-judge")[:1000]
            print(type(books))
            res = dict()
            res['code'] = 200
            res['book_detail'] = dict()
            cnt = 0
            s = {1, 2}
            for book in books:
                if book.img in s:
                    continue
                s.add(book.img)
                res['book_detail'][cnt] = dict()
                res['book_detail'][cnt]['id'] = book.id
                res['book_detail'][cnt]['name'] = book.name
                res['book_detail'][cnt]['author'] = book.author
                res['book_detail'][cnt]['img'] = book.img
                res['book_detail'][cnt]['price'] = book.price
                res['book_detail'][cnt]['score'] = book.score
                res['book_detail'][cnt]['publish_time'] = book.publish_time
                res['book_detail'][cnt]['judge'] = book.judge
                res['book_detail'][cnt]['rec_most'] = book.rec_most
                res['book_detail'][cnt]['rec_more'] = book.rec_more
                res['book_detail'][cnt]['rec_normal'] = book.rec_normal
                res['book_detail'][cnt]['rec_bad'] = book.rec_bad
                res['book_detail'][cnt]['rec_morebad'] = book.rec_morebad
                res['book_detail'][cnt]['readed'] = book.readed
                res['book_detail'][cnt]['reading'] = book.reading
                res['book_detail'][cnt]['readup'] = book.readup
                res['book_detail'][cnt]['mess'] = book.mess
                cnt = cnt + 1
            return JsonResponse({
                "code": 200,
                "data": res,
                "size": cnt
            })
        else:
            # 用户已经登录，那就根据它的历史足迹来返回给他可能喜欢的书籍
            username = request.GET.get("username")
            histories = History.objects.filter(name=username)
            if histories.__len__() == 0:
                books = Book.objects.order_by("-judge")[:1000]
                print(type(books))
                res = dict()
                res['code'] = 200
                res['book_detail'] = dict()
                cnt = 0
                s = {1, 2}
                for book in books:
                    if book.img in s:
                        continue
                    s.add(book.img)
                    res['book_detail'][cnt] = dict()
                    res['book_detail'][cnt]['id'] = book.id
                    res['book_detail'][cnt]['name'] = book.name
                    res['book_detail'][cnt]['author'] = book.author
                    res['book_detail'][cnt]['img'] = book.img
                    res['book_detail'][cnt]['price'] = book.price
                    res['book_detail'][cnt]['score'] = book.score
                    res['book_detail'][cnt]['publish_time'] = book.publish_time
                    res['book_detail'][cnt]['judge'] = book.judge
                    res['book_detail'][cnt]['rec_most'] = book.rec_most
                    res['book_detail'][cnt]['rec_more'] = book.rec_more
                    res['book_detail'][cnt]['rec_normal'] = book.rec_normal
                    res['book_detail'][cnt]['rec_bad'] = book.rec_bad
                    res['book_detail'][cnt]['rec_morebad'] = book.rec_morebad
                    res['book_detail'][cnt]['readed'] = book.readed
                    res['book_detail'][cnt]['reading'] = book.reading
                    res['book_detail'][cnt]['readup'] = book.readup
                    res['book_detail'][cnt]['mess'] = book.mess
                    cnt = cnt + 1
                return JsonResponse({
                    "code": 200,
                    "data": res,
                    "size": cnt
                })
            history_set = {-1, -2}  # 里面存放之前点击过的书籍，这部分数据不应该返回
            tags = {}  # tags存放每个标签对应的数量
            for hh in histories:
                img = hh.img
                if img in history_set:
                    continue
                history_set.add(img)
                # 同一本书它会有对应多个标签，这里需要把这些标签都加进去
                book_set = Book.objects.filter(img=img)
                for book in book_set:
                    tags[book.tag] = tags.get(book.tag, 0) + 1
            total = 0
            for value in tags.values():
                total = total + value
            all_books = list()
            for key in tags.keys():
                cnt = int(tags[key]/total * 200)
                books = Book.objects.filter(tag=key).order_by('-judge')
                for book in books:
                    # 用户已经点过的我就不返回了 并且保证了返回的数据中同一本书只出现一次
                    if book.img in history_set:
                        continue
                    history_set.add(book.img)
                    all_books.append(book)
                    cnt = cnt-1
                    if cnt < 1:
                        break
            gbdt = joblib.load('Algorithm/models/gbdt.model')
            sort_books_dict = dict()
            for book in all_books:
                features = [book.price, book.score, book.judge, book.rec_most, book.rec_more, book.rec_normal,
                            book.rec_bad, book.rec_morebad, book.readed, book.reading, book.readed]
                pro = gbdt.predict_proba(np.array([features]))[0][1]
                sort_books_dict[book.id] = pro
            books = sorted(sort_books_dict.items(), key=lambda one: one[1], reverse=True)
            # for book in books:
            #     print(book[0], sort_books_dict[book[0]])
            res = dict()
            cnt = 0
            res["book_detail"] = dict()
            for item in books:
                iid = item[0]
                book = Book.objects.filter(id=iid)[0]
                res['book_detail'][cnt] = dict()
                res['book_detail'][cnt]['id'] = book.id
                res['book_detail'][cnt]['name'] = book.name
                res['book_detail'][cnt]['author'] = book.author
                res['book_detail'][cnt]['img'] = book.img
                res['book_detail'][cnt]['price'] = book.price
                res['book_detail'][cnt]['score'] = book.score
                res['book_detail'][cnt]['publish_time'] = book.publish_time
                res['book_detail'][cnt]['judge'] = book.judge
                res['book_detail'][cnt]['rec_most'] = book.rec_most
                res['book_detail'][cnt]['rec_more'] = book.rec_more
                res['book_detail'][cnt]['rec_normal'] = book.rec_normal
                res['book_detail'][cnt]['rec_bad'] = book.rec_bad
                res['book_detail'][cnt]['rec_morebad'] = book.rec_morebad
                res['book_detail'][cnt]['readed'] = book.readed
                res['book_detail'][cnt]['reading'] = book.reading
                res['book_detail'][cnt]['readup'] = book.readup
                res['book_detail'][cnt]['mess'] = book.mess
                cnt = cnt + 1
            return JsonResponse({
                "code": 200,
                "data": res,
                "size": cnt
            })


@csrf_exempt
def search(request):
    if request.method == 'GET':
        name = request.GET.get('name')
        print(name)
        books = Book.objects.filter(name__contains=name)
        res = dict()
        res['code'] = 200
        res['book_detail'] = dict()
        cnt = 0
        s = {1, 2}
        for book in books:
            if book.img in s:
                continue
            s.add(book.img)
            res['book_detail'][cnt] = dict()
            res['book_detail'][cnt]['id'] = book.id
            res['book_detail'][cnt]['name'] = book.name
            res['book_detail'][cnt]['author'] = book.author
            res['book_detail'][cnt]['img'] = book.img
            res['book_detail'][cnt]['price'] = book.price
            res['book_detail'][cnt]['score'] = book.score
            res['book_detail'][cnt]['publish_time'] = book.publish_time
            res['book_detail'][cnt]['judge'] = book.judge
            res['book_detail'][cnt]['rec_most'] = book.rec_most
            res['book_detail'][cnt]['rec_more'] = book.rec_more
            res['book_detail'][cnt]['rec_normal'] = book.rec_normal
            res['book_detail'][cnt]['rec_bad'] = book.rec_bad
            res['book_detail'][cnt]['rec_morebad'] = book.rec_morebad
            res['book_detail'][cnt]['readed'] = book.readed
            res['book_detail'][cnt]['reading'] = book.reading
            res['book_detail'][cnt]['readup'] = book.readup
            res['book_detail'][cnt]['mess'] = book.mess
            cnt = cnt + 1
        print(cnt)
        return JsonResponse({
            "code": 200,
            "data": res,
            "size": cnt
        })


def write_to_history(username, date, action, bookname, bookid, img):
    History(name=username, time=date, action=action, bookname=bookname, bookid=bookid, img=img).save()
