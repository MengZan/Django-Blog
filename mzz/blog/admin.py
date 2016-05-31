from django.contrib import admin

from .models import Column,Article,Keyword,MiniArticle,ArticleImage,About

class KeywordInline(admin.TabularInline): 
    model = Keyword
    extra = 3

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title','author', 'pub_date','update_time','is_visable')

    inlines = [KeywordInline]

    list_filter = ['pub_date','author']

    search_fields = ['title']

class ImageInline(admin.TabularInline):  # admin.StackedInline
    model = ArticleImage
    extra = 3

class MiniArticleAdmin(admin.ModelAdmin):   
    list_display = ('content','author','pub_date')

    inlines = [ImageInline]

    list_filter = ['author']

class AboutAdmin(admin.ModelAdmin):   
    list_display = ('author','content')


admin.site.register(Article,ArticleAdmin)
admin.site.register(MiniArticle,MiniArticleAdmin)
admin.site.register(Column)
admin.site.register(About,AboutAdmin)


