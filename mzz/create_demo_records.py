
#!/usr/bin/env python
# -*- coding: utf-8 -*-
 
'''
create some records for demo database
'''
 
from mzz.wsgi import *
from blog.models import Column, Article
 
 
def main():
    columns_urls = [
      ('生活'),
      ('学习'),
      ('影评'),
    ]
 
    for column_name in columns_urls:
        c = Column.objects.get_or_create(name=column_name)[0]
 
        for i in range(1, 11):
            article = Article.objects.get_or_create(
                title='{}_{}'.format(column_name, i),
                content='详细内容： {} {}'.format(column_name, i)
            )[0]
 
            article.columns.add(c)
 
 
if __name__ == '__main__':
    main()
    print("Done!")