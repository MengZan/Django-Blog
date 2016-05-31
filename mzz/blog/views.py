# -*- coding: utf-8 -*-
from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.views import generic
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Column,Article,MiniArticle,Keyword,About

columns = Column.objects.all()

def index(request):   
    articles=Article.objects.filter(is_visable=True)[:3]
    mini_articles=MiniArticle.objects.all()[:2]
    return render(request, 'blog/index.html', {
        'columns': columns,
        'articles':articles,
        'mini_articles':mini_articles,}) 

def column(request, column_id):
    c=get_object_or_404(Column,pk=column_id)
    articles=c.article_set.all()
    paginator=Paginator(articles,10)
    page = request.GET.get('page') 
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        contacts = paginator.page(1)
    except EmptyPage:
        contacts = paginator.page(paginator.num_pages)
    return render(request, 'blog/articles.html', {'column':c,'columns': columns,'articles': contacts,
        'page_range':paginator.page_range,'num_pages':paginator.num_pages}) 

def all_article(request):
    articles=Article.objects.filter(is_visable=True)
    paginator=Paginator(articles,10)  #每一页的数目
    page = request.GET.get('page') 
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        contacts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        contacts = paginator.page(paginator.num_pages)
    return render(request, 'blog/articles.html', {'columns': columns,'articles': contacts,
        'page_range':paginator.page_range,'num_pages':paginator.num_pages}) 

def author_article(request,author):
    articles=Article.objects.filter(is_visable=True,author__username=author)
    paginator=Paginator(articles,10)
    page = request.GET.get('page') 
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        contacts = paginator.page(1)
    except EmptyPage:
        contacts = paginator.page(paginator.num_pages)
    return render(request, 'blog/articles.html', {'columns': columns,'articles': contacts,
        'page_range':paginator.page_range,'num_pages':paginator.num_pages}) 
 
def article(request, article_id):
    a=get_object_or_404(Article,pk=article_id,is_visable=True)
    return render(request, 'blog/article.html', {'columns': columns,'article':a,})

def tips(request):
    mini_articles=MiniArticle.objects.all()
    paginator=Paginator(mini_articles,10)
    page = request.GET.get('page') 
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        contacts = paginator.page(1)
    except EmptyPage:
        contacts = paginator.page(paginator.num_pages)
    return render(request, 'blog/tips.html', {'columns': columns,'mini_articles': contacts,
        'page_range':paginator.page_range,'num_pages':paginator.num_pages}) 

def about(request):
    zz=About.objects.filter(author__username='ZZ')[0]
    mm=About.objects.filter(author__username='MM')[0]
    return render(request, 'blog/about.html',{'columns':columns,'zz':zz,'mm':mm}) 
