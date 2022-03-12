from django.contrib import admin

from .models import Article, Category, Goods, Comment

admin.site.register(Article)
admin.site.register(Category)
admin.site.register(Goods)
admin.site.register(Comment)
# Register your models here.
