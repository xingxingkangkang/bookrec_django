from django.urls import path
from .views import getone, getbooks, history, like, search

urlpatterns = [
    path('getone/', getone),
    path('getbooks/', getbooks),
    path('history/', history),
    path('like/', like),
    path('search/', search)
]
