from urllib import request
from django.db.models import Q
from django.http import Http404
from django.shortcuts import render
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils import tree

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.generics import ListAPIView
from rest_framework.generics import CreateAPIView
from rest_framework.generics import DestroyAPIView
from rest_framework.generics import UpdateAPIView
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication

from .models import Category, Article, Goods, Comment
from .serializers import ArticleSerializer, CreateArticleSerializer, GoodSerializer, CommentSerializer

User = get_user_model()

'''
----------------------Article Line----------------------
'''


class LatestArticlesList(APIView):
    def get(self, request, format=None):
        articles = Article.objects.filter(
            publish=True).order_by('-id').all()[0:16]
        serializer = ArticleSerializer(articles, many=True)
        # serializer = SlimArticleSerializer(articles, many=True)
        return Response(serializer.data)


class ShowArticle(ListAPIView):
    queryset = Article.objects.order_by('-id').all()
    serializer_class = ArticleSerializer


class MyArticleList(APIView):
    authentication_classes = [TokenAuthentication]

    def get(self, request, format=None):
        try:
            article = User.objects.get(username=request.user).articles.order_by('-id').all()
            serializer = ArticleSerializer(article)
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            data = {
                "error":"DoseNotExist",
                "error_message": "このユーザーは存在していません",
            }
            return Response({"status": "error", "data": data}, status=status.HTTP_400_BAD_REQUEST)

class UserArticleList(APIView):
    def post(self, request, format=None):
        try:
            user = User.objects.get(username=request.data['username'])
            if user.locked == False:
                article = user.articles.order_by('-id').all()
                serializer = ArticleSerializer(article)
                return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
            else:
                data = {
                    "error":"DoseNotExist",
                    "error_message": "このユーザーは存在していません",
                }
                return Response({"status": "error", "data": data}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            data = {
                "error":"DoseNotExist",
                "error_message": "このユーザーは存在していません",
            }
            return Response({"status": "error", "data": data}, status=status.HTTP_400_BAD_REQUEST)

class CreateArticle(APIView):
    authentication_classes = [TokenAuthentication]
    def post(self,request,format=None):
        try:
            user = User.objects.get(username=request.user)
            data = {
                "title": request.data['title'],
                "tags": request.data['tags'],
                "content": request.data['content'],
                "author": user.id,
                "category": request.data['category'],
                "publish": request.data['publish'],
            }
            serializer = CreateArticleSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
            else:
                return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            data = {
                "error":"DoseNotExist",
                "error_message": "このユーザーは存在していません",
            }
            return Response({"status": "error", "data": data}, status=status.HTTP_400_BAD_REQUEST)

class UpdateArticle(UpdateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer


class DestroyArticle(DestroyAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer


class ArticleDetail(APIView):
    def get_object(self, article_id):
        try:
            return Article.objects.get(pk=article_id)
        except Article.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        article = self.get_object(pk)
        serializer = ArticleSerializer(article)
        return Response(serializer.data)


@api_view(['POST'])
def search(request):
    query = request.data.get('query', '')

    if query:
        article = Article.objects.filter(publish=True).filter(
            Q(title__icontains=query) | Q(content__icontains=query) | Q(tags__name__in=[query])).distinct("id")
        serializer = ArticleSerializer(article, many=True)
        return Response(serializer.data)
    else:
        return Response({"article": []})


'''
----------------------Good Line----------------------
'''


class CreateGood(CreateAPIView):
    queryset = Goods.objects.all()
    serializer_class = GoodSerializer


class UpdateGood(UpdateAPIView):
    queryset = Goods.objects.all()
    serializer_class = GoodSerializer


class DestroyGood(DestroyAPIView):
    queryset = Goods.objects.all()
    serializer_class = GoodSerializer


class DeleteGood(APIView):
    def get_object(self, user_id, article_id):
        try:
            User = get_user_model()
            goods = User.objects.get(
                id=user_id).goods.filter(article=article_id)
            print(goods)
            return goods
        except User.DoesNotExist:
            raise Http404

    def get(self, request, user_id, article_id, format=None):
        goods = self.get_object(user_id, article_id)
        goods.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class MyGoodList(APIView):
    def get_object(self, user_id):
        try:
            User = get_user_model()
            goods = User.objects.get(
                id=user_id).goods
            return goods
        except User.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        goods = self.get_object(pk)
        serializer = GoodSerializer(goods, many=True)
        return Response(serializer.data)


class MyGoodArticles(APIView):
    def get_object(self, user_id):
        try:
            User = get_user_model()
            goods = User.objects.get(
                id=user_id).goods.order_by('-id').all()
            return goods
        except User.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        goods = self.get_object(pk)
        articles = []
        for good in goods:
            print(good.article.id)
            articles.append(Article.objects.get(id=good.article.id))
        serializer = ArticleSerializer(articles, many=True)
        print("article:", articles)
        return Response(serializer.data)


'''
----------------------Comment Line----------------------
'''


class CreateComment(CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


# class UpdateComment(UpdateAPIView):
#     queryset = Comment.objects.all()
#     serializer_class = CommentSerializer


class DestroyComment(DestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class ArticleComment(APIView):
    def get_object(self, article_id):
        try:
            comments = Article.objects.get(
                id=article_id).comment.all()
            return comments
        except Comment.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        comments = self.get_object(pk)
        serializer = CommentSerializer(comments, many=True)
        print("article:", comments)
        return Response(serializer.data)
