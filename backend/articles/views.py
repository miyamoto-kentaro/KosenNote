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
from .serializers import ArticleSerializer, ArticleDetailSerializer, CreateArticleSerializer, GoodSerializer, CommentSerializer, ArticleAuthenticatedDetailSerializer

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

# articles/create/
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
    authentication_classes = [TokenAuthentication]
    def get_object(self, article_id):
        try:
            article = Article.objects.get(pk=article_id)
            user = User.objects.get(username = self.request.user)
            if article.author == user or article.publish:
                return article
            else:
                raise Http404
        except Article.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        try:
            article = self.get_object(pk)
            serializer = ArticleDetailSerializer(article)
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        except Http404:
            data = {
                "error":"DoseNotExist",
                "error_message": "この記事は存在していません",
            }
            return Response({"status": "error", "data": data}, status=status.HTTP_400_BAD_REQUEST)


# 記事を取得するユーザーと記事の作者が同じ場合に取得できる
class ArticleAuthenticatedDetail(APIView):
    authentication_classes = [TokenAuthentication]
    def get_object(self, article_id):
        try:
            article = Article.objects.get(pk=article_id)
            user = User.objects.get(username = self.request.user)
            print(article.author,user)
            if article.author == user:
                return article
            else:
                raise Http404
        except Article.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        try:
            article = self.get_object(pk)
            serializer = ArticleAuthenticatedDetailSerializer(article)
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        except Http404:
            data = {
                "error":"DoseNotExist",
                "error_message": "この記事は存在していません",
            }
            return Response({"status": "error", "data": data}, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        article = self.get_object(pk)
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



class ShowProfile(APIView):
    authentication_classes = [TokenAuthentication]
    def post(self, request):
        try:
            print(request.auth)
            if(request.auth):
                myuser = User.objects.get(username=request.user)
            else:
                myuser = None

            username = request.data['username']
            profile_user = User.objects.get(username=username)
            if(myuser==profile_user):
                user_article = profile_user.articles.order_by('-id').all()
                user_article_serializer = ArticleSerializer(user_article, many=True)
                goods = Goods.objects.filter(user=profile_user.id)
                goods_article = []
                for good in goods:
                    goods_article.append(good.article)

                goods_article_serializer = ArticleSerializer(goods_article, many=True)
                data = {
                    "profile" : {
                        "username":profile_user.username,
                        "follow":False,
                        },
                    "article_list": user_article_serializer.data,
                    "goods" : goods_article_serializer.data
                }
                return Response({"status": "success", "data": data}, status=status.HTTP_200_OK)
            else:
                user_article = profile_user.articles.filter(publish=True).order_by('-id')
                user_article_serializer = ArticleSerializer(user_article, many=True)
                goods = Goods.objects.filter(user=profile_user.id).first()
                goods = Goods.objects.filter(user=profile_user.id)
                goods_article = []
                for good in goods:
                    if good.article.publish:
                        goods_article.append(good.article)
                goods_article_serializer = ArticleSerializer(goods_article, many=True)
                data = {
                    "profile" : {
                        "username":profile_user.username,
                        "follow":False,
                        },
                    "article_list": user_article_serializer.data,
                    "goods" : goods_article_serializer.data
                }
                return Response({"status": "success", "data": data}, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            data = {
                "error":"DoseNotExist",
                "error_message": "このユーザーは存在していません",
            }
            return Response({"status": "error", "data": data}, status=status.HTTP_400_BAD_REQUEST)

    


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


class CreateGood(APIView):
    authentication_classes = [TokenAuthentication]
    def already_exists(self, article, user):
        try:
            good = Goods.objects.filter(article = article).filter(user=user)
            if good:
                return True
            else:
                return False
        except Goods.DoesNotExist:
            return False

    def get_article(self, article_id):
        try:
            article = Article.objects.get(pk=article_id)
            return article
        except Article.DoesNotExist:
            raise Http404
    def put(self,request,format=None):
        try:
            user = User.objects.get(username=request.user)
            article = self.get_article(request.data['article_id'])
            if self.already_exists(request.data['article_id'],user.id):
                data = {
                    "error":"AlreadyExists",
                    "error_message": "既にGoodしています",
                }
                return Response({"status": "error", "data": data}, status=status.HTTP_400_BAD_REQUEST)
            else:
                data = {
                    "user": user.id,
                    "article":article.id
                }
                serializer = GoodSerializer(data=data)
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
        except Article.DoesNotExist:
            data = {
                "error":"DoseNotExist",
                "error_message": "この記事は存在していません",
            }
            return Response({"status": "error", "data": data}, status=status.HTTP_400_BAD_REQUEST)



class DeleteGood(APIView):
    authentication_classes = [TokenAuthentication]
    def get_object(self, article_id):
        try:
            user = User.objects.get(username=self.request.user)
            goods = user.goods.filter(article=article_id)
            print(goods)
            return goods
        except User.DoesNotExist:
            raise Http404
        except Goods.DoesNotExist:
            raise Http404

    def delete(self, request, format=None):
        try:
            goods = self.get_object(request.data['article_id'])
            goods.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Http404:
            data = {
                "error":"DoseNotExist",
                "error_message": "いいねしていません",
            }
            return Response({"status": "error", "data": data}, status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            print("error")



class GoodAlreadyExists(APIView):
    authentication_classes = [TokenAuthentication]
    def post(self, request):
        try:
            user = User.objects.get(username=self.request.user)
            goods = user.goods.filter(article=request.data['article_id']).first()
            if goods:
                data = {
                    "already_good":True
                }
                return Response({"status": "error", "data": data}, status=status.HTTP_200_OK)
            else:
                data = {
                    "already_good":False
                }
                return Response({"status": "error", "data": data}, status=status.HTTP_200_OK)

        except Goods.DoesNotExist:
            data = {
                "already_good":False
            }
            return Response({"status": "error", "data": data}, status=status.HTTP_200_OK)

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
        try:
            goods = self.get_object(pk)
            serializer = GoodSerializer(goods, many=True)
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        except Http404:
            data = {
                "error":"DoseNotExist",
                "error_message": "ユーザーが存在しません",
            }
            return Response({"status": "error", "data": data}, status=status.HTTP_400_BAD_REQUEST)



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
        # print("article:", articles)
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
