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
                "message": "The username or password is wrong, please check and input again",
                "nickname": ""
            })
        else:
            return JsonResponse({
                "code": 200,
                "message": "succeed",
                "nickname": user[0].nickname
            })


@csrf_exempt
def register(request):
    if request.method == 'POST':
        req = json.load(request)
        username = req['username']
        password = req['password']
        nickname = req['nickname']
        # username = request.POST.get("username")
        # password = request.POST.get("password")
        # nickname = request.POST.get("nickname")
        print(username, password, nickname)
        user = User.objects.filter(username=username)
        if len(user) > 0:
            return JsonResponse({
                "code": 404,
                "message": "The username is already exists"
            })
        else:
            write_to_user(username, password, nickname)
            return JsonResponse({
                "code": 200,
                "message": "write successful",
                "nickname": nickname
            })


def write_to_user(username, password, nickname):
    User(username=username, password=password, nickname=nickname).save()

