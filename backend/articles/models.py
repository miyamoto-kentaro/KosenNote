import json

from django.db import models
from django.conf import settings
from rest_framework import serializers
from taggit.managers import TaggableManager


class Category(models.Model):

    title = models.CharField(max_length=150)
    slug = models.SlugField()

    class Met:
        ordering = {'title', }

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self):
        return f'/{self.slug}/'


class Article(models.Model):
    title = models.CharField(max_length=150)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='articles',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    tags = TaggableManager()

    content = models.TextField()
    publish = models.BooleanField(null=True, blank=True)
    create_at = models.DateField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now_add=True)

    class Met:
        ordering = {'-id', }

    def __str__(self) -> str:
        return self.title

    def get_author_name(self):
        if self.author:
            return self.author.username
        return None


class Goods(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='goods', on_delete=models.CASCADE)
    article = models.ForeignKey(
        Article, related_name='goods', on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class Comment(models.Model):
    title = models.CharField(max_length=150)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    article = models.ForeignKey(
        Article, related_name='comment', on_delete=models.CASCADE)
    comment_to = models.ForeignKey(
        'self', related_name='reply', null=True, blank=True, on_delete=models.SET_NULL)

    content = models.TextField()
    create_at = models.DateField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now_add=True)

    class Meta():
        pass

    def __str__(self) -> str:
        return self.title

    def get_author_name(self):
        if self.author:
            return self.author.username
        return None
