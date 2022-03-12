from rest_framework import serializers
from taggit.serializers import (TagListSerializerField,
                                TaggitSerializer)

from .models import Article, Category, Goods, Comment


class ArticleSerializer(TaggitSerializer, serializers.ModelSerializer):

    tags = TagListSerializerField()

    class Meta:
        model = Article
        fields = ["id",
                  "title",
                  "tags",
                  "content",
                  "create_at",
                  "update_at",
                  "author",
                  "category",
                  "get_author_name",
                  "publish"]


class CreateArticleSerializer(TaggitSerializer, serializers.ModelSerializer):
    tags = TagListSerializerField()

    class Meta:
        model = Article
        fields = ["title",
                  "tags",
                  "content",
                  "author",
                  "category",
                  "publish"]


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ["id",
                  "title",
                  "author",
                  "article",
                  "comment_to",
                  "content",
                  "create_at",
                  "update_at",
                  "get_author_name"]


class GoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goods
        fields = ["user",
                  "article", ]
