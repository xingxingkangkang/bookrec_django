from django.contrib import admin
from books.models import Book, Cate, History


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['image_data', 'name', 'score', 'judge', 'author', "publish_time", 'price', 'tag']
    search_fields = ['name', 'author']
    list_filter = ['tag']
    list_per_page = 30
    actions_on_bottom = True
    actions_on_top = False


@admin.register(Cate)
class CateAdmin(admin.ModelAdmin):
    list_per_page = 50


@admin.register(History)
class HistoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'time', 'action', 'bookname']
