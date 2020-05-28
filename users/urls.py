from django.urls import path
from .views import login, register, modify

urlpatterns = [
    path('login/', login),
    path('register/', register),
    path('modify', modify)
]
