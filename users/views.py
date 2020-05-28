import json

from django.http import JsonResponse
from .models import User
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def login(request):
    if request.method == 'GET':
        name = request.GET.get('username')
        key = request.GET.get('password')
        print(name, key)
        user = User.objects.filter(username=name)
        if len(user) == 0 or key != user[0].password:
            return JsonResponse({
                "code": 404,
                "message": "用户名不存在或密码错误",
                "nickname": ""
            })
        else:
            return JsonResponse({
                "code": 200,
                "message": "登录成功",
                "nickname": user[0].nickname
            })


@csrf_exempt
def register(request):
    if request.method == 'POST':
        req = json.load(request)
        username = req['username']
        password = req['password']
        nickname = req['nickname']
        print(username, password, nickname)
        user = User.objects.filter(username=username)
        print(len(user))
        if len(user) > 0:
            return JsonResponse({
                "code": 404,
                "message": "用户名已存在"
            })
        else:
            write_to_user(username, password, nickname)
            return JsonResponse({
                "code": 200,
                "message": "注册新用户成功",
                "nickname": nickname
            })


@csrf_exempt
def modify(request):
    if request.method == "POST":
        req = json.load(request)
        username = req["username"]
        password = req["password"]
        new_password = req["new"]
        user = User.objects.filter(username=username)
        print(len(user))
        if len(user) == 0 or password != user[0].password:
            return JsonResponse({
                "code": 404,
                "message": "用户名不存在或者旧密码输入错误",
            })
        elif password == new_password:
            return JsonResponse({
                "code": 500,
                "message": "新密码与旧密码相同，请重新输入"
            })
        else:
            User.objects.filter(username=username).update(password=new_password)
            return JsonResponse({
                "code": 200,
                "message": "密码修改成功，下次使用新密码登录"
            })


def write_to_user(username, password, nickname):
    User(username=username, password=password, nickname=nickname).save()

