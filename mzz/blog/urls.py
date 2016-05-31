from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^column/(?P<column_id>[0-9]+)/$',views.column,name='column'),
    url(r'^articles/$',views.all_article,name='all_article'),
    url(r'^articles/(?P<author>\w+)/$',views.author_article,name='author_article'),
    url(r'^article/(?P<article_id>[0-9]+)/$',views.article,name='article'),
    url(r'^tips/$',views.tips,name='tips'),
    url(r'^about/$',views.about,name='about'),
]