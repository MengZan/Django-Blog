# -*- coding: utf-8 -*-
from django.db import models
from django.core.urlresolvers import reverse
from DjangoUeditor.models import UEditorField

import os
from PIL import Image
from django.db.models.fields.files import ImageFieldFile
from mzz.settings import MEDIA_ROOT

class Column(models.Model):
    name=models.CharField('分类名称',max_length=256)
    intro=models.TextField('分类介绍',default='暂无',blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name='文章分类'
        verbose_name_plural='文章分类'   #复数显示名称


class Article(models.Model): 
    columns=models.ManyToManyField(Column,verbose_name='归属分类')  #多对多
    title=models.CharField('标题',max_length=256)
    author=models.ForeignKey('auth.User',blank=True,null=True,verbose_name='作者')  #多对一，调用管理员user？
    content = UEditorField('内容', height=300, width=1000,
        default=u'', blank=True, imagePath="uploads/images/",
        toolbars='besttome', filePath='uploads/files/')
    is_visable=models.BooleanField('是否可见',default=True)
    pub_date=models.DateTimeField('发表时间',null=True)                             #auto_now_add为添加时的时间，更新对象时不会有变动。
    update_time=models.DateTimeField('修改时间',auto_now=True,null=True)  #auto_now无论是你添加还是修改对象，时间为你添加或者修改的时间


    def __str__(self):
        return self.title

    class Meta:
        verbose_name='文章'
        verbose_name_plural='文章'
        ordering = ['-pub_date']

    def get_absolute_url(self):
        path = reverse('blog:article', args=(self.id,))
        return "http://127.0.0.1:8000%s" % path

class Keyword(models.Model):
    word=models.CharField('关键词',max_length=10)
    article=models.ForeignKey(Article)

    def __str__(self):
        return self.word


class MiniArticle(models.Model):
    content=models.TextField('内容',default='想我没')
    author=models.ForeignKey('auth.User',blank=True,null=True,verbose_name='作者')
    pub_date=models.DateTimeField('发表时间',auto_now=True,null=True)

    # def __str__(self):
    #     return self.content[0:10]

    class Meta:
        verbose_name='点滴'
        verbose_name_plural='点滴'
        ordering = ['-pub_date']


class ArticleImage(models.Model):
    image=models.ImageField('插入图片',upload_to='article_img')
    mini_article=models.ForeignKey(MiniArticle)

    thumb=models.ImageField('缩略图',upload_to='thumb_img',blank=True,null=True)

    def save(self):
        super(ArticleImage, self).save()
        img_name=self.image.name.split('/')[1]
        thumb_pixbuf = make_thumb(os.path.join(MEDIA_ROOT,'article_img/'+img_name))
        thumb_path = os.path.join(MEDIA_ROOT,'thumb_img/'+img_name)
        thumb_pixbuf.save(thumb_path)
        self.thumb = ImageFieldFile(self, self.thumb, 'thumb_img/'+img_name)
        super(ArticleImage, self).save()

class About(models.Model):
    image=models.ImageField('头像',upload_to='about_img')
    content = models.TextField('介绍', default='', blank=True)
    author=models.ForeignKey('auth.User',blank=True,null=True,verbose_name='作者')

    def __str__(self):
        return self.author.username

    class Meta:
        verbose_name='我们'
        verbose_name_plural='我们'    

def make_thumb(path,size=150):
    pixbuf = Image.open(path)
    width, height = pixbuf.size

    if height > size:
        delta = height / size
        width = int(width / delta)
        pixbuf.thumbnail((width, height), Image.ANTIALIAS)
        return pixbuf