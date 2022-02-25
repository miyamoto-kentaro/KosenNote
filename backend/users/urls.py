from django.conf import settings
from django.urls import path, include

from . import views

urlpatterns = [
    # emailでユーザーを作成するAPI
    # 仮登録をするAPI
    path('email/pre_register/create', views.CreatePreRegister.as_view()),
    # 仮登録を認証してユーザーを作るAPI
    path('email/pre_register/certification', views.CertificationPreRegister.as_view()),

    # User情報を取得
    # path('me', views.CustomAuthToken.as_view()),

    # emailとusernameでUserを検索して、重複を確認するAPI
    path('already_exists/email', views.UserEmailAlreadyExists.as_view()),
    path('already_exists/username', views.UserNameAlreadyExists.as_view()),
]
