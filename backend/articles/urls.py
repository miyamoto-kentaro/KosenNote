from django.conf import settings
from django.urls import path, include

from . import views

urlpatterns = [
    path('articles/latest/list/', views.LatestArticlesList.as_view()),
    path('articles/list/', views.UserArticleList.as_view()),
    # Profileを取得
    path('profile/',views.ShowProfile.as_view()),
    # path('me/articles/', views.MyArticleList.as_view()),
    path('articles/show-all/', views.ShowArticle.as_view()),
    path('articles/create/', views.CreateArticle.as_view()),
    path('articles/update/<int:pk>/', views.UpdateArticle.as_view()),
    path('articles/destroy/<int:pk>/', views.DestroyArticle.as_view()),
    path('articles/detail/<int:pk>/', views.ArticleDetail.as_view()),
    path('articles/authenticated/detail/<int:pk>/', views.ArticleAuthenticatedDetail.as_view()),
    path('articles/search/', views.search),
    path('articles/goods/users/<int:pk>/', views.MyGoodArticles.as_view()),
    path('goods/already_exists/', views.GoodAlreadyExists.as_view()),
    path('goods/create/', views.CreateGood.as_view()),
    path('goods/destroy/', views.DeleteGood.as_view()),
    path('goods/users/<int:pk>/', views.MyGoodList.as_view()),
    path('comment/article/<int:pk>/', views.ArticleComment.as_view()),
    path('comment/create/', views.CreateComment.as_view()),
    path('comment/destroy/<int:pk>/', views.DestroyComment.as_view()),
]
