from django.db import models
from django.utils.html import format_html


class Cate(models.Model):
    cid = models.IntegerField(blank=False, unique=True, verbose_name='ID')
    name = models.CharField(blank=False, max_length=64, verbose_name='名字')

    class Meta:
        managed = True
        db_table = 'cate'
        verbose_name_plural = "标签类别"

    def __str__(self):
        return self.name


class Book(models.Model):
    name = models.CharField(max_length=64, verbose_name='名字')
    author = models.CharField(max_length=500, verbose_name='作者')
    img = models.CharField(max_length=500, verbose_name='图片')
    price = models.FloatField(verbose_name='价格')
    publish_time = models.CharField(max_length=100, verbose_name='出版日期')
    score = models.FloatField(verbose_name='评分')
    judge = models.IntegerField(verbose_name='评价人数')
    rec_most = models.IntegerField(verbose_name='力荐人数')
    rec_more = models.IntegerField(verbose_name='推荐人数')
    rec_normal = models.IntegerField(verbose_name='还行人数')
    rec_bad = models.IntegerField(verbose_name='较差人数')
    rec_morebad = models.IntegerField(verbose_name='很差人数')
    readed = models.IntegerField(verbose_name='读过')
    reading = models.IntegerField(verbose_name='在读')
    readup = models.IntegerField(verbose_name='想读')
    mess = models.CharField(max_length=1000, verbose_name='图书信息')
    tag = models.CharField(max_length=200, blank=True, null=True, verbose_name='标签')

    class Meta:
        managed = True
        db_table = 'book'
        verbose_name_plural = "图书信息"

    def __str__(self):
        return self.name

    def image_data(self):
        return format_html(
            '<img src="{}" width="80px"/>',
            'https://images.weserv.nl/?url=' + self.img,
        )

    image_data.short_description = u'图片'


class History(models.Model):
    name = models.CharField(max_length=64, verbose_name='名字')
    time = models.DateTimeField(verbose_name='时间')
    action = models.CharField(max_length=64, verbose_name='动作')
    bookname = models.CharField(max_length=64, verbose_name='图书名称')
    bookid = models.IntegerField(verbose_name="图书Id")
    img = models.CharField(max_length=500, verbose_name='图片', default="")

    class Meta:
        managed = True
        db_table = 'history'
        verbose_name_plural = "行为信息"

    def __str__(self):
        return self.name

